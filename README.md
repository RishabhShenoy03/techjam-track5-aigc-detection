# Robust Detection of AI-Generated Images Under Real-World Transformations

TikTok TechJam 2026 — Track 5 submission by team **The First Frame**.

A ResNet18-based binary classifier (real vs. AI-generated) trained on the **CIFAKE** dataset, with
training-time augmentation deliberately drawn from the same transform families the organizers use to
evaluate robustness (JPEG re-encode, Gaussian blur, resize round-trip, Gaussian noise, color jitter,
center crop). Evaluated on all 15 fixed conditions (clean + 14 organizer-specified severities), with a
robustness table, error-analysis failure grids, an out-of-domain sanity check, and a ready-to-use
inference function producing the required JSON output.

Everything lives in one notebook: **`aigc_robust_detector.ipynb`**. It is designed to run start-to-finish
entirely inside a Kaggle Notebook on the free-tier NVIDIA GPU, since Kaggle sessions don't persist state
between runs.

## Running it on Kaggle

1. Go to [kaggle.com/code](https://www.kaggle.com/code), create a new notebook, and upload
   `aigc_robust_detector.ipynb` (File → Upload Notebook), or copy its cells in.
2. **Add the dataset**: click "Add Input" → search for
   [`birdy654/cifake-real-and-ai-generated-synthetic-images`](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images)
   → add it. It will mount at `/kaggle/input/cifake-real-and-ai-generated-synthetic-images`.
3. *(Optional, for the out-of-domain sanity check)* add the org-provided WildFake validation subset
   (COCO val2017 = real, DALL·E Advanced = fake) as a second input. If you don't add it, that cell
   prints a message and skips — everything else still runs.
4. **Enable the GPU**: Settings (right sidebar) → Accelerator → **GPU T4 x2** or **P100**.
5. **Run All.** On a T4, training ~12 epochs of upscaled (128px) CIFAKE plus the full 15-condition eval
   should comfortably fit inside a single session well under the ~9–12h wall-clock and ~30 GPU-h/week
   Kaggle free-tier limits.

## What the notebook produces (in `/kaggle/working`)

- `resnet18_aigc_detector.pt` — best checkpoint (by validation loss)
- `robustness_table.csv` — accuracy/precision/recall/AUC for all 15 conditions
- `robustness_plot.png` — bar chart of accuracy per condition vs. the 85% success bar
- `failures_<condition>.png` — false-positive/false-negative sample grids for the two worst conditions
- `predictions.json` — example output of the inference contract, `[{"image_path", "pred"}]`

## Standalone inference (`predict.py`)

The notebook is the training/eval environment, but the required "score a directory of images"
deliverable is also provided as a standalone CLI, `predict.py`, so it can be run outside Kaggle against
the trained checkpoint. It uses the exact same inference path as the notebook (ResNet18, 128px bicubic
resize, ImageNet normalization, sigmoid → `pred` = P(image is AI-generated)).

```bash
# 1. install dependencies (CPU works out of the box; see requirements.txt for GPU)
pip install -r requirements.txt

# 2. score a directory of images with the checkpoint the notebook produced
python predict.py \
  --image-dir ./test_images \
  --checkpoint resnet18_aigc_detector.pt \
  --output predictions.json
```

This writes the deliverable JSON: `[{"image_path": ..., "pred": <float 0-1>}, ...]`. Useful flags:
`--recursive` to walk subdirectories, `--batch-size` to tune throughput, and `--device {auto,cuda,cpu}`.
Run `python predict.py --help` for the full list. Unreadable/corrupt images are skipped with a warning
rather than aborting the run.

## Design decisions and rationale

See [`.bureau/contracts/direction_v1.md`](.bureau/contracts/direction_v1.md) for the full reasoning
(and [`.bureau/records/teams/team_founding.md`](.bureau/records/teams/team_founding.md) for how the
founding team reached it). Summary of the key calls:

- **CIFAKE only**, upscaled to 128px before training and eval — several organizer-specified transforms
  (0.25x resize, σ=2 blur) are near-meaningless at CIFAKE's native 32x32.
- **ResNet18**, ImageNet-pretrained, fully fine-tuned, single-logit head (~11.7M params, far under the
  2B cap).
- **Robustness via training-time augmentation**: ~50% of batches get one randomly-sampled
  transform-family augmentation at severities distinct from the fixed eval severities, teaching
  invariance without leaking the eval conditions.
- **Pre-registered, falsifiable success bar**: mean accuracy ≥85% across all 15 conditions, no single
  condition more than 15pts below clean. Reported honestly whether met or missed.
- **Out-of-domain sanity check** using the org's own WildFake subset (explicitly demonstration-only),
  reported separately and never used for training.

## Limitations

See the "Limitations" section at the end of the notebook for the full disclosed list — in short:
CIFAKE's domain/resolution/single-generator narrowness, capped eval sample sizes per condition, the
WildFake check being a small demonstration subset rather than a rigorous benchmark, and no
adversarial-robustness claims.

## Devpost deliverable mapping

- **Working prototype** → `aigc_robust_detector.ipynb`, run end-to-end on Kaggle.
- **Scoring script (image dir → JSON of `image_path` + `pred`)** → `predict.py` (see above).
- **Robustness evaluation writeup** → the notebook's robustness table/plot + this README.
- **Error analysis** → the notebook's failure-grid section.
- **Reproducibility** → this README's Kaggle setup steps; the notebook seeds all RNGs (`SEED = 42`).

## Note on how this was built

This project cannot be executed from the environment it was authored in (no Kaggle GPU/credentials
available there). The notebook is handed off ready-to-run; actual accuracy numbers, the pass/fail
verdict on the success bar, and the rendered plots/grids will only exist after you run it on
kaggle.com. Every guarded cell prints a clear message if a required dataset input is missing.
