import whisper
import os
from translator import translate_text
from tts_generator import generate_audio

def process_audio(file_path: str, target_language: str) -> str:
    """
    Processes an audio file: transcribes, translates, and generates new audio.

    Args:
        file_path (str): The path to the audio file.
        target_language (str): The target language for translation.

    Returns:
        str: The path to the generated audio file.
    """
    print(f"Processing audio file: {file_path}")

    # 1. Transcribe audio
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    original_text = result["text"]
    print(f"Original text: {original_text}")

    # 2. Translate text
    translated_text = translate_text(original_text, target_language)
    print(f"Translated text: {translated_text}")

    # 3. Generate new audio
    output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_translated.wav"
    output_path = os.path.join(os.path.dirname(file_path), output_filename)
    generate_audio(translated_text, output_path)

    return output_path
