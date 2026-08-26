# Direction Contract v1

**Track:** TikTok TechJam 2026 — Track 5: Robust Detection of AI-Generated Images Under Real-World Transformations
**Founding team:** The First Frame (see [team_founding.md](../records/teams/team_founding.md))
**Date:** 2026-08-26

## Intent

Ship a working, honestly-evaluated AI-generated-image detector whose defining feature is that it survives TikTok's exact real-world transform battery, built and run entirely inside a single Kaggle Notebook on the free-tier NVIDIA GPU. This is a first-edition, single-session hackathon submission: we optimize for a defensible, reproducible, end-to-end artifact with an honest robustness story — not for a leaderboard-topping clean-accuracy number.

## MVP definition

- **Dataset:** [CIFAKE](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images) (Kaggle-hosted, no download friction) — 120k 32x32 images, real (CIFAR-10) vs. AI-generated (Stable Diffusion). Used for 100% of training. WildFake and SID_Set are out of scope for training in this pass.
- **Resolution handling:** CIFAKE images are upscaled to 128x128 (bicubic) before augmentation, training, and evaluation. Rationale: at native 32x32, several of the org's transforms (0.25x resize, sigma=2 blur) are near-meaningless / destroy signal uniformly for both classes. Upscaling first makes every transform severity in the org's spec meaningfully interpretable.
- **Model:** ResNet18, ImageNet-pretrained, fully fine-tuned, single sigmoid output. ~11M params — far under the 2B cap, fast to train on a T4/P100 within a single Kaggle session, well-precedented on CIFAKE (published transfer-learning results ≥96%).
- **Training-time robustness strategy (the core technical bet):** ~50% of training batches receive one randomly-sampled augmentation drawn from the same transform *families* as the eval battery, at randomized severities distinct from the fixed eval severities (avoids direct leakage while teaching genuine invariance): JPEG re-encode (q 40–95), Gaussian blur (σ 0.3–2.5), resize-down/up (0.4x–0.9x), Gaussian noise (σ 0.01–0.12), brightness/contrast/saturation jitter (±25%), random crop (75–95%). This directly targets the documented failure mode (CIFAKE-trained CNNs collapse to ~25–32% accuracy under blur/downsampling without such augmentation).
- **Evaluation plan (fixed, pre-registered, run once):** held-out CIFAKE test split, evaluated at: clean, JPEG{90,70,50,30}, blur{σ0.5,1.0,2.0}, resize{0.5x,0.25x}, noise{σ0.02,0.05,0.10}, color-jitter(±20%), center-crop(80%) — 14 conditions, each reporting accuracy, precision, recall, AUC. Eval sample size capped at ~3,000 images/condition to fit the Kaggle session time budget; this cap is disclosed, not hidden.
  - **Success threshold (falsifiable):** mean accuracy across all 14 conditions ≥ 85%, and no single condition more than 15 points below clean accuracy. If missed, we report the true number — a disclosed shortfall is an acceptable first-edition outcome; silently hiding one is not.
- **Out-of-domain sanity check:** the org-provided WildFake validation subset (COCO val2017 = real, DALL·E Advanced = fake — explicitly demonstration-only in the brief, never used for training) is run through the same pipeline and reported separately, labeled "out-of-domain / non-headline," to demonstrate the team is aware of and transparent about the CIFAKE domain-mismatch risk rather than ignoring it.
- **Output format:** a notebook cell / equivalent function taking an image directory and producing a JSON list `[{"image_path": ..., "pred": <float 0-1>}]`, threshold-free.
- **Deliverables:** one self-contained Kaggle notebook (data load → train → eval → inference, since Kaggle sessions don't persist state across runs), a README (setup, repro steps, limitations), a robustness table, and an error-analysis section with sample failure grids per transform.

## Constraints & boundaries all future work must respect

- Must run entirely inside Kaggle's website/notebook environment using the free-tier NVIDIA GPU (single session, ~9–12h wall-clock ceiling, ~30 GPU-h/week quota). No local-only steps in the critical path.
- No external training data beyond CIFAKE; no pretrained weights trained on the eval benchmarks' labels (matches org's hard rule).
- No multi-dataset joint training, no ensembling, no ViT/production-serving scope creep in this pass — explicitly deferred.
- Model parameter count must stay far under the 2B cap (ResNet18 ≈ 11M).
- If time runs short inside the Kaggle session, cut in this order: (1) eval sample size per condition, (2) OOD sanity-check sample size — never cut coverage of the 14 required transform conditions themselves.
- No secrets, API keys, or credentials committed anywhere in the notebook or repo.

## Open questions for operational teams to carry forward

- Actual robustness numbers are unknown until the notebook is run on Kaggle's GPU (this environment has no Kaggle execution access) — the notebook is being handed off ready-to-run; the human must execute it on kaggle.com and capture real output.
- Whether 8–12 epochs is sufficient for convergence on upscaled 128px CIFAKE is an empirical question to be resolved by the training run itself (early stopping on val loss is built in to guard against under/over-shooting).
- Whether the 85%/15pt bar is achievable with a single ResNet18 pass, or whether a quick augmentation-strength iteration is needed, will only be known after first run — the notebook is structured so re-running just the eval/augmentation cells (not retraining from scratch) is cheap.
