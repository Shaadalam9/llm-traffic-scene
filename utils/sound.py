import numpy as np
from moviepy.editor import VideoFileClip
from scipy.io import wavfile
import os
import common
from custom_logger import CustomLogger
from logmod import logs

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger


class Video_sound():

    def __init__(self) -> None:
        pass

    def audio_db_from_video(self, video_path):
        """
        Extracts the audio track from a video file, computes its RMS (root mean square) amplitude,
        and returns the loudness in decibels relative to digital full scale (dBFS).

        The function works as follows:
            1. Loads the video and extracts its audio track.
            2. Saves the audio temporarily as a WAV file (16-bit PCM).
            3. Loads the WAV file and converts it to a mono (single channel) signal if necessary.
            4. Normalises the audio data to the range [-1, 1] based on its data type.
            5. Calculates the RMS value of the audio waveform.
            6. Converts the RMS value to dBFS (where 0 dBFS is the maximum possible amplitude).
            7. Cleans up the temporary audio file.
            8. Returns the dBFS value. If the audio track is missing, raises an exception.

        Args:
            video_path (str): Path to the video file.

        Returns:
            float: The RMS loudness of the video's audio track, in dBFS (typically negative).

        Raises:
            ValueError: If the video has no audio track.
            Exception: For other file I/O or decoding errors.
        """
        # Load the video file
        video = VideoFileClip(video_path)
        audio = video.audio

        # If there is no audio track, raise an exception
        if audio is None:
            raise ValueError(f"No audio track found in {video_path}")

        # Save the audio as a temporary WAV file (16-bit PCM)
        temp_audio = "temp_audio.wav"
        audio.write_audiofile(temp_audio, fps=44100, nbytes=2, codec='pcm_s16le', logger=None)

        # Read the audio data from the temporary file
        sr, data = wavfile.read(temp_audio)

        # If the audio is stereo (2D), convert to mono by averaging the channels
        if len(data.shape) == 2:
            data = data.mean(axis=1)

        # Normalise the audio to floating point values in [-1, 1]
        if data.dtype == np.int16:
            # Standard 16-bit PCM
            data = data.astype(np.float32) / 32768
        elif data.dtype == np.int32:
            # 32-bit PCM
            data = data.astype(np.float32) / 2147483648
        elif data.dtype == np.uint8:
            # 8-bit PCM (unsigned): 0-255 to -1 to 1
            data = (data.astype(np.float32) - 128) / 128
        elif np.issubdtype(data.dtype, np.floating):
            # If already float, ensure max amplitude is <= 1
            max_abs = np.max(np.abs(data))
            if max_abs > 1:
                data = data / max_abs
        else:
            # Unknown or exotic format
            logger.debug(f"Unknown dtype: {data.dtype}, shape: {data.shape}")
            data = data.astype(np.float32)

        # Calculate RMS (Root Mean Square) of the audio waveform
        rms = np.sqrt(np.mean(data ** 2))

        # Convert RMS to dBFS (decibels relative to full scale)
        # 0 dBFS means maximum possible amplitude; typical audio is negative
        db = 20 * np.log10(rms) if rms > 0 else -np.inf

        # Remove the temporary file to clean up
        os.remove(temp_audio)

        # Return the loudness in dBFS
        return db
