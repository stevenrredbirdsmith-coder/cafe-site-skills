# Topview Pricing Map — captured live 2026-10-01 (read-only API read, session-authenticated)

## Status change (IMPORTANT)
The **Ultra annual free-unlimited lane is GONE** — Unlimited Mode now shows
LOCKED ("Busy / Heavy queue right now" + green "Upgrade to Unlimited" upsell).
Steve confirmed 2026-10-01: "my topview deal is over". Topview is now a
**PAID-per-credit lane** on our account (balance at capture: 792.25 credits).
The Seedance 2.0 "free queue" path is no longer free for us.

## Plans (from subscription.charge.productList, USD via Stripe, cents)
| Plan | Monthly | Annual (per year) |
|---|---|---|
| Basic | $18.00 (1800c) | $216.00 |
| Plus | $36.00 (3600c) | $432.00 |
| Team | $…monthly visible | ~$1512/yr CNY-eq |
| 3-Day Pro Trial | one-time (BRL 5.28) | — |

## i2v generate pricing (from board UI, Seedance family)
- Seedance 2.5 (paid default!): 45 credits @ 30s
- Seedance 2.0: 15 credits per generate (15s default) — was the free-queue
  model; now metered.
- Duration options on Seedance 2.0: 15s (default), resolution HD 720p,
  aspect 9:16 / 16:9.

## Video UPSCALE pricing (per second, USD — from aiVideo.getAiVideoConfig)
| Model | 720p/30 | 1080p/30 | 2K/30 | 4K/30 | 720p/60 | 1080p/60 | 2K/60 | 4K/60 |
|---|---|---|---|---|---|---|---|---|
| Tencent Pro | 0.05 | 0.10 | 0.20 | 0.40 | 0.10 | 0.20 | 0.40 | 0.80 |
| Tencent Std | 0.02 | 0.04 | 0.08 | 0.16 | 0.04 | 0.08 | 0.16 | 0.32 |
| Volcengine | 0.02 | 0.04 | 0.08 | 0.16 | 0.04 | 0.08 | 0.16 | 0.32 |

(Upscale accepts up to 600s, 4K, .mp4/.mov/.avi/.webm, 500MB max;
Realistic vs Anime style modes.)

## Board recipe (verified live, stage-by-stage, screenshots in CAFE evidence)
board/10c8ffba46254274b62e457d3d41dbae → Video tool → Image to Video tab →
model chip (dropdown: Featured/All models) → Seedance 2.0 → duration 15s →
aspect 9:16/16:9 → Generate split-button: Credit Mode (priority, credits)
vs Unlimited Mode (LOCKED for this account now).

## Decision for Steve
Topview generation now costs credits (15/gen for Seedance 2.0 i2v 15s).
Either: treat topview as a budgeted metered lane (set monthly credit cap),
or retire it from the free-lane skill and lean on remaining free lanes
(a2e v1, perchance) + local 5090. Balance 792.25 credits ≈ 53 Seedance 2.0
generations if spent deliberately.
