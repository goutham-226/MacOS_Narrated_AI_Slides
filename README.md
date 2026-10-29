# Voice AI — "Lisa", a narrated terminal explainer

Lisa is a small macOS command-line assistant that turns a topic you type into a
narrated slideshow, right in your terminal:

1. You type a topic.
2. An LLM (Qwen3 235B via [Replicate](https://replicate.com)) writes a ~250-second
   narrator script about it.
3. The same LLM turns that script into 25 image prompts.
4. An image model (FLUX.2 Pro via Replicate) generates an image for each prompt.
5. macOS text-to-speech reads the script aloud while the images are drawn in the
   terminal one after another.

## Requirements

- macOS (speech uses the built-in `say` voices through `macos-speech`)
- Python 3.9+
- [iTerm2](https://iterm2.com) to see the images. `term-image` draws them using
  iTerm2's inline image protocol, so in other terminals (including the default
  macOS Terminal) the slideshow won't display properly. The narration still works.
- A [Replicate API token](https://replicate.com/account/api-tokens)

> Replicate charges per prediction. One run makes 2 LLM calls and 25 image
> generations, so check current pricing before running it a lot.

## Setup

```bash
git clone https://github.com/<your-username>/voice_ai.git
cd voice_ai

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and set REPLICATE_API_TOKEN
```

## Usage

```bash
python v_ai.py
```

Lisa introduces herself, then prompts `Type:`. Enter a topic (for example
`how black holes form`) and press Enter. Generation takes a few minutes; images
are saved as `output_img0.png` … `output_img24.png` in the project folder and the
narration starts once they are ready.

## Configuration

| Variable              | Required | Description                          |
| --------------------- | -------- | ------------------------------------ |
| `REPLICATE_API_TOKEN` | yes      | Your Replicate API token             |

Variables are read from the environment, or from a `.env` file in the project
root (loaded with `python-dotenv`). `.env` is git-ignored — never commit it.

## Project layout

| File                | Purpose                                                        |
| ------------------- | -------------------------------------------------------------- |
| `v_ai.py`           | Main app: script generation, image generation, speech, display |
| `prompt_parser.py`  | Work-in-progress parser for `<vprompt>` tagged prompts         |
| `video_output.py`   | Experiment: plays `output_v.mp4` frame by frame with OpenCV    |
| `term_img.py`, `img_google_out.py` | Experiments: render an image in the terminal    |

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the pipeline works.

## Known flaws

- **Slow responses.** Every model call runs one after another and blocks until
  it finishes: two LLM calls, then 25 image generations, each waiting on its own
  Replicate prediction. Nothing is shown or spoken until all 25 images are done,
  so a single run can take several minutes. Generating images concurrently (or
  starting narration while images are still being made) would cut this down.
- **No handling of Replicate request limits.** Replicate rate-limits prediction
  requests, and `v_ai.py` makes no attempt to deal with that: there is no retry,
  backoff, or throttling around `LLM.run(...)`. If a request is rejected (for
  example with HTTP 429 Too Many Requests) the exception is unhandled, the
  script exits, and the images generated so far are not reused on the next run.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
