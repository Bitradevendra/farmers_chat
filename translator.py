from deep_translator import GoogleTranslator, PonsTranslator

def translate_text(text: str, target_language: str) -> str:
    """
    Translates the given text to the target language with retry logic.

    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., 'es', 'fr').

    Returns:
        str: The translated text.
    """
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # For Indian languages, use a more suitable translation approach
            indian_languages = ['te', 'hi', 'ur', 'mr', 'bn', 'ta', 'kn', 'gu', 'pa']
            
            if target_language in indian_languages:
                # For Indian languages, use PonsTranslator which often provides better translations
                try:
                    translator = PonsTranslator(source='en', target=target_language)
                    translated = translator.translate(text)
                    if translated and translated.strip():
                        return translated
                except Exception as pons_error:
                    print(f"Pons translation failed (attempt {attempt+1}): {pons_error}")
                    
            # Default to GoogleTranslator
            translator = GoogleTranslator(source='auto', target=target_language)
            translated = translator.translate(text)
            
            if translated and translated.strip():
                return translated
            
        except Exception as e:
            print(f"Translation attempt {attempt+1} failed: {e}")
            
        if attempt < max_retries - 1:
            print(f"Retrying translation in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
    print(f"All translation attempts failed. Returning original text.")
    return text
