from TTS.api import TTS
import torch
import os
import requests
from typing import Optional
from typing import Dict, Any
import json

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates text from source language to target language using Google Translate API.
    
    Args:
        text (str): The text to translate
        source_lang (str): The source language code
        target_lang (str): The target language code
        
    Returns:
        str: Translated text
    """
    try:
        print(f"Translating text from {source_lang} to {target_lang}")
        print(f"Input text: {text}")
        
        # Supported Indian languages
        supported_languages = {
            'en': 'en',   # English
            'te': 'te',   # Telugu
            'hi': 'hi',   # Hindi
            'ta': 'ta',   # Tamil
            'mr': 'mr',   # Marathi
            'bn': 'bn',   # Bengali
            'kn': 'kn',   # Kannada
            'gu': 'gu',   # Gujarati
            'pa': 'pa'    # Punjabi
        }

        # Validate languages
        if source_lang not in supported_languages:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang not in supported_languages:
            raise ValueError(f"Unsupported target language: {target_lang}")

        # Use Google Translate API
        import googletrans
        from googletrans import Translator
        
        translator = Translator()
        
        # Translate text
        translated = translator.translate(
            text,
            src=supported_languages[source_lang],
            dest=supported_languages[target_lang]
        )
        
        print(f"Translated text: {translated.text}")
        return translated.text

    except Exception as e:
        print(f"Error in translation: {e}")
        # As a fallback, return the original text
        return text

def process_text_file(input_file: str, output_file: Optional[str] = None, target_lang: str = 'en') -> str:
    """
    Processes a text file by translating its content to the target language and saving it.
    
    Args:
        input_file (str): Path to the input text file
        output_file (Optional[str]): Path to save the translated text file. If None, saves with _translated suffix
        target_lang (str): Target language code for translation
        
    Returns:
        str: Path to the generated translated file
    """
    # Validate input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Determine output file path
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_{target_lang}.txt"
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise IOError(f"Error reading input file: {e}")
    
    # Translate content
    source_lang = 'en'  # Default source language
    translated_content = translate_text(content, source_lang, target_lang)
    
    # Save translated content
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"Translated text saved to: {output_file}")
        return output_file
    except Exception as e:
        raise IOError(f"Error saving translated file: {e}")

def generate_audio(text: str, output_path: str, target_language: str = 'en', source_language: str = 'auto'):
    """
    Generates audio from the given text and saves it to a file.
    If source language is not 'auto', it will translate the text to target language first.

    Args:
        text (str): The text to convert to speech.
        output_path (str): The path to save the generated audio file.
        target_language (str): The target language for speech.
        source_language (str): The source language for translation (if needed).
    """
    try:
        # Validate output path
        if not output_path.lower().endswith(('.wav', '.mp3')):
            raise ValueError("Output path must end with .wav or .mp3 extension")
            
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # Translate text if source language is specified and different from target
        if source_language != 'auto' and source_language != target_language:
            try:
                print(f"Translating text from {source_language} to {target_language}...")
                translated_text = translate_text(text, source_language, target_language)
                text = translated_text
                print(f"Translated text: {text}")
            except Exception as e:
                print(f"Warning: Text translation failed: {e}")
                print("Proceeding with original text...")

        # Add required classes to safe globals for PyTorch 2.6+
        from TTS.tts.configs.xtts_config import XttsConfig
        from TTS.tts.models.xtts import XttsAudioConfig
        torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])

        # Init TTS with Indian languages support
        print("Initializing TTS model...")
        try:
            # Add required classes to safe globals for PyTorch 2.6+
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
            from TTS.config.shared_configs import BaseDatasetConfig
            
            # Add all required classes to safe globals
            safe_globals = [XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]
            torch.serialization.add_safe_globals(safe_globals)
            
            # Load the model with weights_only=False
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            
            # Set weights_only=False explicitly in the model's load_checkpoint method
            import torch
            torch.serialization.set_weights_only(False)
            
            print("TTS model loaded successfully")
            return tts
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to default model loading...")
            
            # Try loading without weights_only parameter
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            return tts
        
        # Indian language codes supported by XTTS v2
        indian_languages = {
            'te': 'Telugu',
            'hi': 'Hindi',
            'ur': 'Urdu',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'pa': 'Punjabi'
        }

        # Add more languages supported by XTTS v2
        supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'pl': 'Polish',
            'ru': 'Russian',
            'tr': 'Turkish',
            'ar': 'Arabic',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean'
        }
        supported_languages.update(indian_languages)
        
        # Validate language
        if target_language not in supported_languages:
            raise ValueError(f"Unsupported language: {target_language}. Supported languages: {', '.join(supported_languages.keys())}")
            
        print(f"Generating audio in {supported_languages[target_language]}")

        # Run TTS
        # You can specify a speaker_wav if you want to clone a voice.
        # For now, we'll use the default speaker.
        # Find the correct language code in the TTS model
        language_code = next((lang for lang in tts.languages if lang.startswith(target_language)), None)
        if not language_code:
            raise ValueError(f"Language {target_language} not found in available languages: {tts.languages}")
        
        # Run TTS with specified language
        print(f"Generating audio using language: {language_code}")
        print(f"Text length: {len(text)} characters")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        
        # Attempt to generate audio
        try:
            tts.tts_to_file(text=text, file_path=output_path, speaker=tts.speakers[0], language=language_code)
            
            # Verify if file was actually created
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Failed to create audio file at {output_path}")
                
            # Get file size
            file_size = os.path.getsize(output_path)
            if file_size == 0:
                raise ValueError(f"Generated audio file is empty: {output_path}")
                
            print(f"Generated audio saved successfully to {output_path}")
            print(f"File size: {file_size/1024:.2f} KB")
            return True
            
        except Exception as e:
            # Clean up any empty file if it exists
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                    print(f"Removed empty/invalid file: {output_path}")
                except Exception as cleanup_error:
                    print(f"Error cleaning up file: {cleanup_error}")
            raise e
    except Exception as e:
        print(f"Error during audio generation: {str(e)}")
        import traceback
        print("Detailed error:", traceback.format_exc())
        return False
