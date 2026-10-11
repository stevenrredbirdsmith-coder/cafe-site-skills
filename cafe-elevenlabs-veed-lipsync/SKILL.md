---
name: cafe-elevenlabs-veed-lipsync
description: "PROVEN 2026-10-10: CAFE Grid desk-4 (ElevenLabs) lipsync workflow — CDP-attach to the grid webview, inject cookies, select Veed Lipsync, upload clip+audio, generate, download. Use when making a talking/lipsynced video in CAFE."
version: 1.0.0
---

# CAFE × ElevenLabs Veed Lipsync — proven workflow

End-to-end pipeline PROVEN 2026-10-10 (job completed, 6.7 MB mp4 retrieved, 14.5s):

**Inputs:** a source clip (mp4) + speech audio (mp3, timed to clip length).
**Output:** lipsynced mp4 with audio.

## Transport: CDP attach to the LIVE grid (session reuse)

The desk-4 webview holds the logged-in ElevenLabs session. **Playwright cannot launch
the Electron partition while the grid runs (file locks), so attach via CDP instead:**

1. Relaunch grid with a debug port:
   `npx electron main.js --remote-debugging-port=9444` (cwd `A:\_SPA\CAFE\grid_test`)
2. `GET http://127.0.0.1:9444/json/list` — targets of type **`webview`** (not `page`)
   are the desk panes. Find the one whose URL contains `elevenlabs`.
3. Open a websocket to its `webSocketDebuggerUrl` and drive with
   `Runtime.evaluate` / `Page.captureScreenshot` / `DOM.setFileInputFiles`.

Full driver: `C:\Users\rredb\AppData\Local\Temp\el_cdp17.py` (pattern: class CDP +
evaljs + shot). If the pane shows sign-in (session refresh), inject auth cookies first:

```
Network.setCookie {name: fern_token|xi_website_user, value: <from partition cookie DB>,
domain: elevenlabs.io, path: /, secure: true}
```
Cookie values live in plaintext in
`~/AppData/Roaming/Electron/Partitions/desk-4/Network/Cookies` (SQLite, copy to temp first).

## UI automation map (verified selectors)

- **Model picker trigger:** `[data-testid="image-video-model-picker-trigger"]`
- **Model search inside dialog:** any `input` in `[role=dialog]` — set value via the
  native value setter + `input` event, type `Veed` to filter
- **Veed Lipsync option:** `[cmdk-item][data-value="Veed Lipsync"]` (41 credits/s —
  NOT "Veed Lipsync 2.0" at 424/s, NOT "Sync Lipsync 2 Pro" at 661/s)
- **File slots after Veed selected:** 2 inputs — one accepts `video/mp4…` (clip),
  one accepts `audio/mpeg…` (speech). Use `DOM.setFileInputFiles` with fresh nodeIds
  (DOM re-renders after each upload — re-query before the second file!)
- **Generate button:** `button[aria-label="Generate"]` (36×36, bottom-right of composer).
  Close any open dialog first (Escape) or you may hit a DIFFERENT model's generate —
  verify the model chip reads "Veed Lipsync" BEFORE clicking.

## Cost gate

- Veed Lipsync ≈ **41 credits/s**. 15s clip ≈ 615 credits. Verify the model chip and
  inputs BEFORE generate. The picker defaults to Gemini Omni Flash — always re-select.
- Steve's approval required for any single job > 500 credits.

## Gotchas learned (all hit on 10-10)

1. **Dialog-steals-click:** the model dialog stays open over the composer; the "Generate"
   you find may belong to another model (nearly fired Seedance 2.5 at ~100k credits).
   Always Escape-close + verify chip text first.
2. **DOM.setFileInputFiles nodeIds go stale** after the first upload — re-query
   `DOM.querySelectorAll` for the audio slot.
3. **Video download:** the history page's `<video>` src is a signed GCS URL (~917 chars,
   DO NOT truncate). Plain `urllib` GET with a UA header works — no cookies needed.
   In-page `fetch`/XHR is CORS-blocked.
4. **TTS:** the ElevenLabs MCP OAuth token lacks TTS scopes. Use Celle's own
   `text_to_speech` tool (edge provider), then tempo-match with
   `ffmpeg -filter:a atempo=<ratio>` to hit exact clip length.
5. **Audio length matters:** lipsync syncs to the SHORTER of clip/audio — tempo-match
   the audio to the clip duration (e.g. 22s voice → atempo 1.47 → 15s).

## Deliverables from the proven run

- Clip: `A:\_SPA\CAFE\artifacts\topview_wan3_omni_celle.mp4` (Topview Wan3 omni-ref)
- Voice: `celle_to_steve_15s_fast.mp3` (14.97s, tempo-matched)
- Result: `A:\_SPA\CAFE\artifacts\veed_lipsync_celle.mp4` (6.7 MB, 14.5s, AAC audio)


## Run 2 lessons (2026-10-10 evening, QA-hardened rerun)

1. **Workflow proven end-to-end**: model chip select via search box ("Veed") → cmdk item →
   chip text assert; DOM.getDocument + DOM.querySelector(nodeId=) shape (response is {"nodeId": N},
   not {"node": {nodeId}}); DOM.setFileInputFiles per input (2 inputs: [0]=video, [1]=audio);
   submit = `button[aria-label="Generate"]` (black circle, up-arrow SVG) — NOT the rightmost
   round button (that's "Show Suggestions"), and NOT textless black buttons.
2. **The composer is a bottom drawer over Explore** — vision QA of the full page will misread it
   as "gallery, FAIL". Crop `clip={y: innerHeight-220, width: innerWidth, height: 220}` to QA the drawer.
3. **Credits charge on COMPLETION, not submit**: 267 left stayed through processing; after done = 44
   (223 spent ≈ 41cr/s × 15s + fees). A "N% done" badge appears in the History tab while processing.
4. **Download path**: click the card's `aria-label="Download"` button → Electron saves to
   ~/Downloads/ElevenLabs_video_veed-lipsync_<UTC>.mp4. Watch Downloads dir for new files.
5. **Download-order trap**: history cards are a grid; first Download button ≠ newest job.
   VERIFY the downloaded file's frames before claiming it's the new one (this bit us: got the
   old gothic-video job twice).
6. **Moderation gate (the real blocker)**: ElevenLabs blocked the muxed lipsync output with
   "This generation may violate our Terms of Service" — user-confirmed cause: the generated
   woman read as too realistic (moderation passed only because STT audio read as fantasy).
   The video-only preview asset still completed. Future runs: tame the voiceover content and/or
   stylize the character to keep moderation happy. NOT a workflow bug.
7. **Audio+video delivery shape**: completed lipsync = muxed mp4 via Download; the <video> src
   in DOM is a silent preview (no audio stream) — don't QA audio from the preview asset.


## THEORY PROVEN (2026-10-10 ~22:00): tame rerun SUCCEEDED
- Same neon clip + TAME edge-tts audio (en-US-AriaNeural, wholesome line, tempo-matched 16.9->14.95s)
- Same flow: chip select -> DOM.setFileInputFiles -> aria-label=Generate -> charged 223 (266->43)
- Result: MUXED mp4 (video+aac, 15.08s) surfaced as content_asset in History; mouth visibly
  articulating at 7.5s frame; audio track real speech (-23dB mean).
- CONCLUSION: content moderation blocks mux/audio on too-realistic sensual content; tame passes.
- Recipe: edge-tts generate -> atempo to clip length -> same upload flow. Frame-QA at multiple
  timestamps (5s/10s stills can both land on closed-mouth pauses).
- Delivery: preview assets from History <video> src (content_asset/... asset_preview.mp4) CAN be
  the final muxed file — check streams with ffprobe, don't assume preview=silent.
