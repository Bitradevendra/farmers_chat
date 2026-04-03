import os
from translator import translate_text
from tts_generator import generate_audio

def process_text(file_path: str, target_language: str) -> str:
    """
    Processes a text file: reads, translates, and generates audio.

    Args:
        file_path (str): The path to the text file.
        target_language (str): The target language for translation.

    Returns:
        str: The path to the generated audio file.
    """
    print(f"Processing text file: {file_path}")

    # 1. Read text from file
    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    print(f"Original text: {original_text}")

    # 2. Translate text
    translated_text = translate_text(original_text, target_language)
    print(f"Translated text: {translated_text}")

    # 3. Generate audio
    output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_translated.wav"
    output_path = os.path.join(os.path.dirname(file_path), output_filename)
    generate_audio(translated_text, output_path)

    return output_path
