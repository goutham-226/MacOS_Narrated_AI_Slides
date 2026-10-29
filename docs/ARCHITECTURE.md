# Architecture

`v_ai.py` runs as a single linear script.

```
topic (stdin)
   │
   ▼
Qwen3-235B (Replicate) ── "write a narrator-only script for 250 seconds"
   │  script_to_talk
   ▼
Qwen3-235B (Replicate) ── "create 25 image prompts in <prmpt></prmpt> tags"
   │  llm_output → parsed into array_prmpts
   ▼
FLUX.2 Pro (Replicate) ── one call per prompt → output_imgN.png
   │
   ▼
two threads started together:
   ├─ talk():           macOS speech synthesizer reads script_to_talk
   └─ display_images(): draws each image in the terminal for 10 s, then clears
```

## Steps

1. **Intro and input** — the macOS `Synthesizer` (voice "Alex") speaks a short
   greeting, then reads a topic from stdin. The script instruction is appended to
   it and leading/trailing spaces are stripped.
2. **Script generation** — `qwen/qwen3-235b-a22b-instruct-2507` with
   `temperature=0.1`, `max_tokens=1024`. The streamed output is joined into one
   string.
3. **Prompt generation** — the script is sent back to the same model, asking for
   25 image prompts wrapped in `<prmpt>…</prmpt>` tags.
4. **Prompt parsing** — a character scan collects the text between each `>` and
   the next `</`, giving one entry per prompt.
5. **Image generation** — each prompt goes to `black-forest-labs/flux-2-pro`
   (1 MP, 1:1). The result is written to `output_img<N>.png`.
6. **Playback** — speech and the slideshow run in parallel threads. Each image is
   shown for 10 seconds, so 25 images cover roughly the 250-second script.
   Images are drawn with `term-image`, which relies on iTerm2's inline image
   protocol, so the slideshow only displays correctly in iTerm2.

## Secrets

The Replicate token is read from `REPLICATE_API_TOKEN` (environment or `.env`).
The script exits with a message if it is missing.
