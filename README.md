# Farmers Chat

A practical multilingual media-processing pipeline that can take a file from the real world and turn it into translated, spoken output.

## Why This Project Exists

`farmers_chat` is built around a very direct idea: people should be able to hand the system a video, audio clip, text file, or image and get something useful back in another language without navigating a complicated stack.

## What It Does

- detects whether the input is video, audio, text, or image
- translates supported content into a target language
- generates speech output for translated text
- routes each input type through the right processor automatically

## Project Structure

```text
farmers_chat/
|-- main.py
|-- video_processor.py
|-- audio_processor.py
|-- text_processor.py
|-- translator.py
|-- tts_generator.py
|-- requirements.txt
|-- Indic-TTS/
`-- README.md
```

## Requirements

- Python 3.8+
- FFmpeg in your system `PATH`

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
python main.py --file_path "path\to\input.mp4" --target_language "te"
```

Examples:

```bash
python main.py --file_path "sample.txt" --target_language "hi"
python main.py --file_path "sample.mp3" --target_language "ta"
```

## How It Works

- `main.py` classifies the file by extension and routes it to the right pipeline.
- `video_processor.py`, `audio_processor.py`, and `text_processor.py` handle the actual transformation steps.
- `translator.py` manages language conversion.
- `tts_generator.py` turns translated text into playable audio.
- `Indic-TTS/` provides deeper speech tooling for multilingual output workflows.

## Best Fit

This project is especially compelling where accessibility, regional language support, and low-friction media translation matter more than polished dashboards.
