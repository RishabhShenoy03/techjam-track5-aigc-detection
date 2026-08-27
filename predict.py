#!/usr/bin/env python3
"""
predict.py — AIGC detection inference CLI.

Takes a directory of images and writes a JSON file with a confidence score for
each image indicating the likelihood that it is AI-generated.

Output format (the Track-5 deliverable contract):
    [
      {"image_path": "<path>", "pred": <float in [0, 1]>},
      ...
    ]
where `pred` = P(image is AI-generated). Threshold-free: downstream consumers
pick their own operating point.

This mirrors the inference logic in aigc_robust_detector.ipynb exactly
(ResNet18, 128px bicubic resize, ImageNet normalization, single sigmoid logit),
but as a standalone script that loads the trained checkpoint produced by the
notebook (resnet18_aigc_detector.pt).

Usage:
    python predict.py --image-dir path/to/images \
                      --checkpoint resnet18_aigc_detector.pt \
                      --output predictions.json

    # recurse into subdirectories:
    python predict.py --image-dir path/to/images --recursive

Run `python predict.py --help` for all options.
"""

import argparse
import glob
import json
import os
import sys

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms as T
from torchvision.models import resnet18

# --- Constants (must match training in aigc_robust_detector.ipynb) ---
IMG_SIZE = 128
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def build_model(device):
    """Recreate the exact architecture used at training time: ResNet18 with a
    single-logit head. Weights are loaded from the checkpoint, so we do NOT
    download the ImageNet-pretrained weights here (weights=None)."""
    model = resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    return model.to(device)


def load_checkpoint(model, checkpoint_path, device):
    """Load a state_dict checkpoint. Tolerates checkpoints saved either as a
    bare state_dict (what the notebook saves) or wrapped in a dict under common
    keys."""
    if not os.path.isfile(checkpoint_path):
        sys.exit(
            f"ERROR: checkpoint not found at '{checkpoint_path}'.\n"
            f"Train the model first (run aigc_robust_detector.ipynb on Kaggle) "
            f"and point --checkpoint at the resulting resnet18_aigc_detector.pt."
        )
    ckpt = torch.load(checkpoint_path, map_location=device)
    if isinstance(ckpt, dict) and not any(k.endswith("weight") or k.endswith("bias") for k in ckpt):
        # wrapped: try common container keys
        for key in ("state_dict", "model_state_dict", "model"):
            if key in ckpt:
                ckpt = ckpt[key]
                break
    model.load_state_dict(ckpt)
    model.eval()
    return model


def list_images(image_dir, recursive=False):
    if not os.path.isdir(image_dir):
        sys.exit(f"ERROR: --image-dir '{image_dir}' is not a directory.")
    paths = []
    if recursive:
        for root, _dirs, files in os.walk(image_dir):
            for fname in files:
                if fname.lower().endswith(IMAGE_EXTENSIONS):
                    paths.append(os.path.join(root, fname))
    else:
        for fname in os.listdir(image_dir):
            full = os.path.join(image_dir, fname)
            if os.path.isfile(full) and fname.lower().endswith(IMAGE_EXTENSIONS):
                paths.append(full)
    return sorted(set(paths))


@torch.no_grad()
def predict_dir(model, image_dir, device, batch_size=128, recursive=False):
    """Run the model over every image in image_dir and return a list of
    {"image_path": ..., "pred": float} dicts. pred = P(image is AI-generated)."""
    paths = list_images(image_dir, recursive=recursive)
    if not paths:
        print(f"No images found in '{image_dir}' "
              f"(looked for extensions: {', '.join(IMAGE_EXTENSIONS)}).")
        return []

    normalize = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    results = []
    for i in range(0, len(paths), batch_size):
        batch_paths = paths[i:i + batch_size]
        tensors, kept_paths = [], []
        for p in batch_paths:
            try:
                img = Image.open(p).convert("RGB").resize((IMG_SIZE, IMG_SIZE), Image.BICUBIC)
            except Exception as e:  # unreadable/corrupt image — skip, don't crash the run
                print(f"WARNING: skipping unreadable image '{p}': {e}", file=sys.stderr)
                continue
            tensors.append(normalize(img))
            kept_paths.append(p)
        if not tensors:
            continue
        xb = torch.stack(tensors).to(device)
        logits = model(xb).squeeze(1)
        probs = torch.sigmoid(logits).cpu().numpy()
        for p, prob in zip(kept_paths, probs):
            results.append({"image_path": p, "pred": float(prob)})
        print(f"  processed {min(i + batch_size, len(paths))}/{len(paths)} images", end="\r")

    print()  # newline after the progress carriage-returns
    return results


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Score images for likelihood of being AI-generated (AIGC detection).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--image-dir", "-i", required=True,
                        help="Directory of images to score.")
    parser.add_argument("--checkpoint", "-c", default="resnet18_aigc_detector.pt",
                        help="Path to the trained model checkpoint (.pt state_dict).")
    parser.add_argument("--output", "-o", default="predictions.json",
                        help="Path to write the JSON predictions file.")
    parser.add_argument("--batch-size", "-b", type=int, default=128,
                        help="Inference batch size.")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Recurse into subdirectories of --image-dir.")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"],
                        help="Compute device. 'auto' uses CUDA if available.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    print(f"Device: {device}")

    model = build_model(device)
    model = load_checkpoint(model, args.checkpoint, device)
    print(f"Loaded checkpoint: {args.checkpoint}")

    results = predict_dir(
        model, args.image_dir, device,
        batch_size=args.batch_size, recursive=args.recursive,
    )

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {len(results)} predictions -> {args.output}")


if __name__ == "__main__":
    main()
