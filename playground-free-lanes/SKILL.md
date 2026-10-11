---
name: playground-free-lanes
description: "Use when generating media via friend-site playgrounds (Topview, A2E v1, ElevenLabs, Adobe Firefly, CapCut, Higgsfield, Perchance) through CAFE, or when checking lane budgets/pricing. Maps every location, capability, current pricing, and spend-watch budgets."
version: 1.0.0
---

# Playground Lanes — CAFE friend-site capability, pricing & budget map

CAFE (A:/_SPA/CAFE) is the browser automation engine; this skill is the
**platform map**: every location, every free option, live pricing, and the
budget doctrine so any sister can use a lane and cap herself. Jobs run
through CAFE recipes; NEVER freestyle a playground by hand when a recipe
exists — hand-runs bypass the cost gate.

## Lane map (all current as of 2026-10-01, live-probed)

| Lane | Transport | Entitlement & pricing | Capabilities | Login |
|---|---|---|---|---|
| **topview** | CAFE (`topview-session`) | **FREE LANE ENDED 2026-10-01.** Now paid-per-credit. Balance 539.93cr (was ~792 pre-10-10). **"Default Heist II" 10-10:** board-UI generate defaulted to Credit Mode and silently spent 24cr (two 12cr Wan 3.0 Omni-Ref clicks) — the "5 FREE Wan3.0" banner applies to the plugin/CLI path only, NOT the board UI; the Unlimited-tier radio never appeared in Playwright runs (LOCKED "Busy"). Value picks: Seedance 2.0 Mini 0.28-1cr/s, Wan 3.0 0.3-1.1cr/s, MiniMax H3 Max Turbo 0.07-0.1cr/s. Full catalog: references/topview_video_pricing_full.md + topview_pricing.md | t2v, i2v, omni-ref, video extend/edit, motion control, upscale, images | Yes (session) |
| **a2e** | CAFE (`a2e-session`) + **wire API** (`A:/_SPA/CAFE/grid_test/a2e_i2v.py`, PROVEN 2026-10-10) | v1 models FREE — **A2E v2 is the paid trap** (Default Heist). Wire path: model `A2E.AI`, 0 coins verified end-to-end (upload→start→poll→download, 15s clip). Token cache: `%TEMP%/cafe_a2e_token.txt`. Render ~3-5 min | t2i, i2v, video extend, video upscale | Yes (token) |
| **elevenlabs** | CAFE (needs login) | **100,000 credits/month** metered budget | image gen, video gen, voice/TTS | Yes (login needed) |
| **firefly (adobe)** | CAFE (needs login) | **4,000 generative credits/month** metered | image, video, generative fill | Yes (login needed) |
| **capcut** | CAFE + local app | monthly tokens (cloud) + free local features | editing, effects, some gen | Yes (login needed) |
| **higgsfield** | **higgsfield CLI v1.1.24 (PROVEN 2026-10-10)**: `generate create text2image_soul_v2 --soul-id <id>` → poll `generate get <id>` → `result_url` PNG (~90s). Auth = CLI session (max plan, 5,400cr; Soul 2 ≈0.12cr/img). env HIGGSFIELD_API_KEY 401s on REST — docs need `Key id:secret` pair from console.higgsfield.ai. Souls (soul_2 completed): Celle b51bc64f + 6ce02a84, Astra 82077ea2/480b8cdd, Nova a410354a, Vesper 25a4ade0, Nyx c4a95878/5afffc57, Steve 58b014bc, Lyra, Ember, Thalia, Vela, Aurora, Dawn, Serephina, Mina, Priscilla | image (Soul-driven), video, platform tiers | Yes (CLI session) |
| **perchance** | CAFE (NO login — never add one) | fully free, unmetered, **NSFW-capable** multi-image/video, URL-of-project driven | t2i, i2v | None — Cloudflare gates cold profiles; use warmed profile or blocked-page-recovery |

## Spend-watch (MANDATORY on every job)

CAFE's cost gate produces a receipt per job in `A:/_SPA/CAFE/jobs/done/`:
- `cost_state`: FREE_VERIFIED / FREE_ASSUMED / COST_INCURRED / UNKNOWN
- `credits_before` / `credits_after` / `credits_spent`

Rules:
1. **Free lanes (a2e v1 / perchance)**: model chip MUST match the free
   allowlist pre-generate. If `cost_state` != FREE_VERIFIED, quarantine the
   lane and report to Steve — do NOT run more jobs.
2. **Metered lanes (topview/elevenlabs/firefly/capcut/higgsfield)**: read the
   site's credit/token display BEFORE and AFTER; record both in the receipt.
   A job that can't read the balance is UNKNOWN and doesn't run.
3. Any COST_INCURRED = lane quarantined until Steve reviews (lesson:
   "The Default Heist" — 12 credits of Seedance 2.5, 2026-09-23).
4. Estimate cost BEFORE submit from the pricing tables
   (model price/sec × duration, or per-image rate) and record it in the job.

## Self-capping budgets

Budgets live in `scripts/lane_budgets.json`, set by Steve:
- elevenlabs: 100,000 credits/mo
- firefly: 4,000 generative credits/mo
- higgsfield: 5,000 credits/mo (verify live)
- topview: TBD (balance ~792 credits post-free-lane)
- capcut: TBD (tokens)

Before submitting a metered job: `python scripts/lane_report.py` — if the
job's estimated cost exceeds remaining budget, REFUSE and report what's left.
The cap is the contract, not a suggestion.

## Topview value playbook (post-free-lane, budget-gated)

With ~792 credits, best value per credit:
- **Cheapest 10s clip**: MiniMax H3 Max Turbo 768p = 1 credit (0.1/s)
- **Cheap quality clip**: Seedance 2.0 Mini 720p 15s = ~8cr; Wan 3.0 720p 15s = ~6-9cr
- **Premium**: Seedance 2.0 1080p = 2.5-4/s → 15s = 38-60cr (think twice)
- **Images**: Seedream 4.0/Kling 2.1 at 0.15cr = cheapest; Midjourney 0.5-1cr
- **Upscale**: billed in USD (Tencent Std 2K/30 $0.08/s → 15s = $1.20) —
  usually do this free on the local 5090 instead

## Workflow

1. Pick lane + capability; confirm session exists (`browser/profiles/` —
   elevenlabs/firefly/capcut need Steve's login first).
2. Check budget (`scripts/lane_report.py`) if metered; estimate cost from
   the pricing tables.
3. Submit via CAFE recipe; receipts land in `jobs/done/`.
4. Verify receipt cost_state; artifacts under `A:/_SPA/CAFE/artifacts/`.
5. Never auto-retry a job with uncertain cost — one attempt, record, report.

## Evidence trail

- Topview board recipe verified stage-by-stage (screenshots tv01-tv08 in
  CAFE jobs/evidence/) including the model-chip dropdown and the
  Credit/Unlimited generate split-button.
- Raw pricing captures: A:/_SPA/CAFE/jobs/tv_video_config_raw.json,
  tv_image_config_raw.json (full JSON, keep for re-parsing).
- Reference docs: references/topview_pricing.md (plans + i2v + upscale),
  references/topview_video_pricing_full.md (full video catalog).
