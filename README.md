# farmers_chat

`farmers_chat` is a Python media translation and text-to-speech pipeline for video, audio, text, and image files.

## Install

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Use

```bash
python main.py --file_path "path\to\input.mp4" --target_language "te"
```

## How It Works

- `main.py` detects the input type.
- `video_processor.py`, `audio_processor.py`, and `text_processor.py` handle each media path.
- `translator.py` and `tts_generator.py` provide translation and speech output.
