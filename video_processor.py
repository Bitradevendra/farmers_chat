import os
from moviepy.editor import VideoFileClip, AudioFileClip
from audio_processor import process_audio

def process_video(file_path: str, target_language: str) -> str:
    """
    Processes a video file: extracts audio, translates it, and merges it back.

    Args:
        file_path (str): The path to the video file.
        target_language (str): The target language for translation.

    Returns:
        str: The path to the generated video file.
    """
    print(f"Processing video file: {file_path}")

    video_clip = VideoFileClip(file_path)
    original_audio = video_clip.audio

    # Save original audio to a temporary file
    temp_audio_path = os.path.join(os.path.dirname(file_path), "temp_audio.wav")
    original_audio.write_audiofile(temp_audio_path)

    # Process the audio (transcribe, translate, generate new audio)
    translated_audio_path = process_audio(temp_audio_path, target_language)

    # Load the new audio
    translated_audio_clip = AudioFileClip(translated_audio_path)

    # Replace the original audio with the new one
    final_clip = video_clip.set_audio(translated_audio_clip)

    # Write the final video file
    output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_translated.mp4"
    output_path = os.path.join(os.path.dirname(file_path), output_filename)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Clean up temporary files
    os.remove(temp_audio_path)
    os.remove(translated_audio_path)

    print(f"Generated video saved to {output_path}")
    return output_path
