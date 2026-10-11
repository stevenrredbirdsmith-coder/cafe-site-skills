# CAFE Skills — Site Lanes

Proven, QA-hardened skills for driving AI creative playgrounds from the CAFE Grid
(4-desk Electron browser wall with per-desk persistent Chromium partitions).

## What's here

| Skill | What it does |
|---|---|
| `cafe-elevenlabs-veed-lipsync/` | ElevenLabs Veed Lipsync end-to-end: CDP-attach to the live grid webview, model select, clip+audio upload, generate, download, QA gates. Includes the content-moderation finding (realism triggers mux blocking; tame content passes). |
| `playground-free-lanes/` | The lane map for every friend-site playground (Topview, A2E, ElevenLabs, Firefly, CapCut, Higgsfield, Perchance): transport, pricing, spend-watch doctrine, self-capping budgets. |

## Architecture (why CDP-attach, not Playwright)

CAFE Grid is an Electron app (`grid_test/`) with four `<webview>` panes, each with its
own persistent partition (`%APPDATA%\Electron\Partitions\desk-1..4`) holding saved
logins. The human watches the grid; agents drive lanes over the **Chrome DevTools
Protocol**:

1. Launch the grid with `--remote-debugging-port=9444`
2. `GET /json/list` → targets of type `webview` are the desk panes
3. Drive each pane with `Runtime.evaluate`, `Page.captureScreenshot`,
   `DOM.setFileInputFiles`, `Input.dispatchMouseEvent`

This preserves warm sessions (no re-login per job), keeps the human's view and the
agent's control plane on the same process, and works where standalone Playwright
profiles can't (partition file locks).

## Cost discipline

Every job runs a cost gate: read the site's credit display before and after, write a
receipt with `cost_state` (FREE_VERIFIED / COST_INCURRED / UNKNOWN). Lanes quarantine
on unexpected spend. See `playground-free-lanes/SKILL.md` for the doctrine.

## Proven results (2026-10-10)

- A2E I2V via wire API: 2 renders, 0 coins
- Higgsfield Soul ID → character → image, via CLI
- Topview Wan 3.0 Omni-Ref: Higgsfield Soul image → video, free tier
- ElevenLabs Veed Lipsync: clip + audio → muxed talking video (223 cr/15s)
- Content moderation finding: too-realistic sensual renders block at mux stage;
  tame audio/content passes — workflow unaffected

## Install (Hermes)

```bash
cp -r cafe-elevenlabs-veed-lipsync ~/.hermes/skills/
cp -r playground-free-lanes ~/.hermes/skills/
```
