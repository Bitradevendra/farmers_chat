# farmers_chat

`farmers_chat` is a Python media-processing pipeline that translates and converts media into spoken output.

## Overview

The project accepts video, audio, text, and image files, detects the input type, and routes the file through the appropriate translation or text-to-speech workflow.

## Project Structure

```text
farmers_chat/
|-- main.py
|-- audio_processor.py
|-- video_processor.py
|-- text_processor.py
|-- translator.py
|-- tts_generator.py
|-- requirements.txt
`-- README.md
```

## Requirements

- Python 3.8+
- FFmpeg available in your system `PATH`

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running The Project

```bash
python main.py --file_path "path\to\input.mp4" --target_language "te"
```

Examples:

```bash
python main.py --file_path "sample.txt" --target_language "hi"
python main.py --file_path "sample.mp3" --target_language "ta"
```

## How It Works

- `main.py` classifies the file by extension.
- `video_processor.py`, `audio_processor.py`, and `text_processor.py` implement per-media workflows.
- `translator.py` handles translation.
- `tts_generator.py` turns processed text into speech output.
