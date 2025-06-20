import common
from custom_logger import CustomLogger
from logmod import logs
import os
import statistics
import pandas as pd
import pycountry
import subprocess
import json
import unicodedata
from utils.sound import Video_sound
import numpy as np

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger
sound_class = Video_sound()


class Video_info:
    def __init__(self) -> None:
        pass

    @staticmethod
    def convert_to_mb(size):
        """
        Converts a file size from bytes to megabytes (MB), rounded to two decimal places.

        Args:
            size (int): File size in bytes.

        Returns:
            float: File size in MB.
        """
        return round(size / (1024 * 1024), 2)

    def analyse_video_files(self, folder_path, video_extensions=None):
        """
        Analyzes video files in a given folder, returning the average file size (MB),
        standard deviation of file sizes (MB), the file with the maximum size,
        and the file with the minimum size, along with their sizes in MB.

        Args:
            folder_path (str): Path to the folder to scan.
            video_extensions (tuple, optional): File extensions to consider as videos.
                Defaults to common video formats.

        Returns:
            dict: A dictionary containing:
                - average_size_MB (float)
                - std_dev_size_MB (float)
                - max_size_file (str)
                - max_size_MB (float)
                - min_size_file (str)
                - min_size_MB (float)
        """
        if video_extensions is None:
            # Common video file extensions
            video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg', '.mpg')

        files_info = []
        db_results = {}

        # List all files in the directory and check if they are video files
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(video_extensions):
                full_path = os.path.join(folder_path, filename)
                info = self.get_video_info(full_path)
                self.print_video_info(info)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    files_info.append((filename, size))
                    try:
                        name_without_ext, _ = os.path.splitext(filename)
                        db = sound_class.audio_db_from_video(full_path)
                        db_results[name_without_ext] = float(db) if isinstance(db, np.floating) else db
                    except Exception:
                        name_without_ext, _ = os.path.splitext(filename)
                        db_results[name_without_ext] = None  # or log the error

        if not files_info:
            logger.info("No video files found in folder: %s", folder_path)
            return

        sizes_mb = [Video_info.convert_to_mb(size) for _, size in files_info]
        avg_size_MB = round(statistics.mean(sizes_mb), 2)
        std_dev_size_MB = round(statistics.stdev(sizes_mb), 2) if len(sizes_mb) > 1 else 0.0
        max_file, max_size = max(files_info, key=lambda x: x[1])
        min_file, min_size = min(files_info, key=lambda x: x[1])

        logger.info(f"The average size of the videos is {avg_size_MB} MB.")
        logger.info(f"The standard deviation in the size of the videos is {std_dev_size_MB} MB.")
        logger.info(f"The largest video file is '{max_file}' with size {Video_info.convert_to_mb(max_size)} MB.")
        logger.info(f"The smallest video file is '{min_file}' with size {Video_info.convert_to_mb(min_size)} MB.")

        valid_db_results = {k: v for k, v in db_results.items() if v is not None}
        if valid_db_results:
            max_db_file = max(valid_db_results, key=valid_db_results.get)  # type: ignore
            min_db_file = min(valid_db_results, key=valid_db_results.get)  # type: ignore
            max_db_value = valid_db_results[max_db_file]
            min_db_value = valid_db_results[min_db_file]

            logger.info(f"The file with the maximum dB value is '{max_db_file}' with {max_db_value} dB.")
            logger.info(f"The file with the minimum dB value is '{min_db_file}' with {min_db_value} dB.")
        else:
            logger.info("No valid dB values were computed for the video files.")

        return db_results

    def video_processing_time_stats(self, df):
        """
        Calculate statistics related to video processing times from a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing at least the columns
                'City' and 'Video processing time (in s)'.

        Returns:
            dict: Dictionary with keys:
                - 'average': Mean video processing time (float)
                - 'std_dev': Standard deviation of processing times (float)
                - 'max_city': City with the longest processing time (str)
                - 'max_value': Maximum processing time (float)
                - 'min_city': City with the shortest processing time (str)
                - 'min_value': Minimum processing time (float)

        The function ensures that the 'Video processing time (in s)' column is numeric,
        safely handles non-numeric or missing values, and identifies the cities with
        the longest and shortest processing times.
        """

        # Ensure the 'Video processing time (in s)' column is numeric.
        # Non-numeric values (e.g., missing or malformed entries) will be converted to NaN.
        df['Video processing time (in s)'] = pd.to_numeric(df['Video processing time (in s)'], errors='coerce')

        # Calculate the mean (average) processing time, ignoring NaNs.
        avg_time = df['Video processing time (in s)'].mean()

        # Calculate the standard deviation of processing times, ignoring NaNs.
        sd_time = df['Video processing time (in s)'].std()

        # Find the row (city) with the maximum processing time.
        max_row = df.loc[df['Video processing time (in s)'].idxmax()]

        # Find the row (city) with the minimum processing time.
        min_row = df.loc[df['Video processing time (in s)'].idxmin()]

        logger.info(f"The average video processing time is {avg_time:.2f} seconds.")
        logger.info(f"The standard deviation of video processing time is {sd_time:.2f} seconds.")
        logger.info(f"The city with the longest processing time is '{max_row['City']}' with {max_row['Video processing time (in s)']:.2f} seconds.")  # noqa:E501
        logger.info(f"The city with the shortest processing time is '{min_row['City']}' with {min_row['Video processing time (in s)']:.2f} seconds.")  # noqa:E501

    def get_video_info(self, video_path):
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format:stream',
            '-of', 'json',
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info = json.loads(result.stdout)

        format_info = info.get('format', {})
        streams = info.get('streams', [])

        video_stream = next((s for s in streams if s['codec_type'] == 'video'), None)
        audio_stream = next((s for s in streams if s['codec_type'] == 'audio'), None)

        data = {
            'file': os.path.basename(video_path),
            'duration': float(format_info.get('duration', 0)),
            'size_MB': round(int(format_info.get('size', 0)) / (1024 * 1024), 2),
            'bitrate_kbps': round(int(format_info.get('bit_rate', 0)) / 1000, 2) if format_info.get('bit_rate') else None,  # noqa:E501
            'container': format_info.get('format_name', ''),
        }
        if video_stream:
            data.update({
                'video_codec': video_stream.get('codec_name', ''),
                'width': video_stream.get('width', ''),
                'height': video_stream.get('height', ''),
                'resolution': f"{video_stream.get('width', '')}x{video_stream.get('height', '')}",
                'fps': eval(video_stream['r_frame_rate']) if 'r_frame_rate' in video_stream else '',
                'aspect_ratio': video_stream.get('display_aspect_ratio', ''),
                'color_space': video_stream.get('color_space', ''),
                'color_depth': f"{video_stream.get('bits_per_raw_sample', '')} bit" if video_stream.get('bits_per_raw_sample') else '',  # noqa:E501
                'chroma_subsampling': video_stream.get('chroma_subsampling', ''),
            })
        if audio_stream:
            data.update({
                'audio_codec': audio_stream.get('codec_name', ''),
                'audio_channels': audio_stream.get('channels', ''),
                'audio_sample_rate': audio_stream.get('sample_rate', ''),
                'audio_language': audio_stream.get('tags', {}).get('language', ''),
            })
        return data

    def count_cities_by_continent(self, df):
        """
        Counts how many cities are from each continent in the provided CSV file.

        Args:
            csv_file (str): Path to the CSV file.

        Returns:
            pandas.Series: Number of cities per continent.
        """
        counts = df['Continent'].value_counts()

        logger.info("Number of cities per continent:")
        for continent, count in counts.items():
            logger.info(f"- {continent}: {count}")

    def get_value(self, df, column_name1, column_value1, column_name2, column_value2, target_column):
        """
        Retrieves a value from the target_column based on the condition
        that both column_name1 matches column_value1 and column_name2 matches column_value2.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the mapping file.
        column_name1 (str): The first column to search for the matching value.
        column_value1 (str): The value to search for in column_name1.
        column_name2 (str or None): The second column to search for the matching value (optional).
        column_value2 (str or None): The value to search for in column_name2. If "unknown",
                                     the value is treated as NaN.
        target_column (str): The column from which to retrieve the corresponding value.

        Returns:
        Any: The value from target_column that corresponds to the matching values in both
             column_name1 and column_name2.
        """
        # Normalise column_name1 values
        df[column_name1] = df[column_name1].astype(str).map(self.normalise_str)
        column_value1 = self.normalise_str(column_value1)

        # If no second condition is given
        if column_name2 is None and column_value2 is None:
            filtered_df = df[df[column_name1] == column_value1]
        else:
            # Normalize column_name2 values
            df[column_name2] = df[column_name2].astype(str).map(self.normalise_str)
            if column_value2 == "unknown":
                column_value2 = float('nan')
            else:
                column_value2 = self.normalise_str(column_value2)

            if pd.isna(column_value2):
                filtered_df = df[(df[column_name1] == column_value1) & (df[column_name2].isna())]
            else:
                filtered_df = df[(df[column_name1] == column_value1) & (df[column_name2] == column_value2)]

        if not filtered_df.empty:
            return filtered_df.iloc[0][target_column]
        else:
            return None

    def iso2_to_flag(self, iso2):
        if iso2 is None:
            # Return a placeholder or an empty string if the ISO-2 code is not available
            logger.debug("Set ISO-2 to Kosovo.")
            return "🇽🇰"
        return chr(ord('🇦') + (ord(iso2[0]) - ord('A'))) + chr(ord('🇦') + (ord(iso2[1]) - ord('A')))

    def iso3_to_iso2(self, iso3_code):
        try:
            # Find the country by ISO-3 code
            country = pycountry.countries.get(alpha_3=iso3_code)

            # Return the ISO-2 code
            return country.alpha_2 if country else None

        except AttributeError or LookupError as e:
            logger.debug(f"Converting up ISO-3 {iso3_code} to ISO-2 returned error: {e}.")
            return None

    def print_video_info(self, info):
        logger.info(f"File: {info.get('file')}")
        logger.info(f"  Duration: {info.get('duration')} sec")
        logger.info(f"  Size: {info.get('size_MB')} MB")
        logger.info(f"  Bitrate: {info.get('bitrate_kbps')} kbps")
        logger.info(f"  Container: {info.get('container')}")
        logger.info(f"  Video Codec: {info.get('video_codec')}")
        logger.info(f"  Resolution: {info.get('resolution')}")
        logger.info(f"  FPS: {info.get('fps')}")
        logger.info(f"  Aspect Ratio: {info.get('aspect_ratio')}")
        logger.info(f"  Color Space: {info.get('color_space')}")
        logger.info(f"  Color Depth: {info.get('color_depth')}")
        logger.info(f"  Chroma Subsampling: {info.get('chroma_subsampling')}")
        logger.info(f"  Audio Codec: {info.get('audio_codec')}")
        logger.info(f"  Audio Channels: {info.get('audio_channels')}")
        logger.info(f"  Audio Sample Rate: {info.get('audio_sample_rate')}")
        logger.info(f"  Audio Language: {info.get('audio_language')}")
        logger.info('-' * 50)

    def strip_accents(self, text):
        """
        Removes accents/diacritics from a string.
        """
        if not isinstance(text, str):
            return text
        text = unicodedata.normalize('NFD', text)
        return ''.join([c for c in text if not unicodedata.combining(c)])

    def normalise_str(self, text):
        """
        Normalise to NFC, lowercase, strip whitespace, and remove accents.
        """
        if not isinstance(text, str):
            return text
        text = unicodedata.normalize('NFC', text.strip().lower())
        text = self.strip_accents(text)
        return text
