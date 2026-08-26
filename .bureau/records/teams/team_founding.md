# Team: The First Frame

**Type:** Founding team
**First day:** 2026-08-26
**Mandate:** Convene once at project genesis to resolve ambiguity in the problem statement (TikTok TechJam 2026, Track 5) and produce the direction contract for all operational teams to build against.

## Members

| Name | Role | First day |
|---|---|---|
| Priya Nakamura | Strategist | 2026-08-26 |
| Desmond Okoro | Researcher | 2026-08-26 |
| Farrah Lindqvist | Critic | 2026-08-26 |

## Summary of session

- **Priya Nakamura (Strategist)** drafted the MVP: CIFAKE-only training, ResNet18 backbone, transform-family augmentation during training, 14-condition robustness eval with a pre-registered success bar (≥85% mean accuracy, ≤15pt max drop).
- **Desmond Okoro (Researcher)** confirmed via prior literature (Wang et al. CVPR 2020; CIFAKE follow-up robustness study) that training-time JPEG/blur/resize/noise augmentation is the established, proven way to achieve this kind of robustness, and flagged that CIFAKE models are known to collapse under blur/downsampling *without* it — validating Priya's core technical bet.
- **Farrah Lindqvist (Critic)** flagged the central risk: CIFAKE's native 32x32 resolution makes several org-specified transforms (resize 0.25x, heavy blur) nearly meaningless, and the model may learn resolution-specific artifacts that don't generalize to real-world (e.g. Midjourney/DALL-E-scale) images. Recommended upscaling before transform application (which the Strategist's plan already did) and adding an explicit out-of-domain sanity check.

## Resolution

The team converged on upscaling CIFAKE to 128px before both training-time augmentation and eval, and on using the org-provided WildFake COCO-vs-DALL-E validation subset (explicitly demonstration-only in the brief) as a free, ready-made out-of-domain generalization check — resolving Farrah's core objection without needing to source new data.

Full detail in [`direction_v1.md`](../../contracts/direction_v1.md).
