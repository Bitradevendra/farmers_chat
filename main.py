import argparse
import os
import shutil
from video_processor import process_video
from audio_processor import process_audio
from text_processor import process_text

def get_file_type(file_path):
    """Identifies the file type based on its extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    video_exts = ['.mp4', '.mkv', '.avi', '.mov']
    audio_exts = ['.mp3', '.wav', '.m4a', '.flac']
    text_exts = ['.txt']
    image_exts = ['.jpg', '.jpeg', '.png', '.gif']

    if ext in video_exts:
        return 'video'
    elif ext in audio_exts:
        return 'audio'
    elif ext in text_exts:
        return 'text'
    elif ext in image_exts:
        return 'image'
    else:
        return 'unsupported'

def main():
    """Main function to run the processing pipeline."""
    parser = argparse.ArgumentParser(description='Process video, audio, or text files for translation and TTS.')
    parser.add_argument('--file_path', type=str, required=True, help='Path to the input file.')
    parser.add_argument('--target_language', type=str, required=True, help='Target language for translation (e.g., \'es\', \'fr\').')

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: File not found at {args.file_path}")
        return

    file_type = get_file_type(args.file_path)

    if file_type == 'video':
        output_path = process_video(args.file_path, args.target_language)
        print(f"\nFinal video saved at: {output_path}")
    elif file_type == 'audio':
        output_path = process_audio(args.file_path, args.target_language)
        print(f"\nFinal audio saved at: {output_path}")
    elif file_type == 'text':
        output_path = process_text(args.file_path, args.target_language)
        print(f"\nFinal audio saved at: {output_path}")
    elif file_type == 'image':
        output_filename = f"{os.path.splitext(os.path.basename(args.file_path))[0]}_output{os.path.splitext(args.file_path)[1]}"
        output_path = os.path.join(os.path.dirname(args.file_path), output_filename)
        shutil.copy(args.file_path, output_path)
        print(f"Image file copied to: {output_path}")
    else:
        print(f"Unsupported file type for: {args.file_path}")

if __name__ == "__main__":
    main()
