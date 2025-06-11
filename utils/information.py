import common
from custom_logger import CustomLogger
from logmod import logs
import os
import statistics
import pandas as pd

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger


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
        # List all files in the directory and check if they are video files
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(video_extensions):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    files_info.append((filename, size))

        # If no video files found, return default values
        if not files_info:
            return {
                "average_size_MB": 0,
                "std_dev_size_MB": 0,
                "max_size_file": None,
                "max_size_MB": 0,
                "min_size_file": None,
                "min_size_MB": 0
            }

            # Get list of sizes in MB
        sizes_mb = [Video_info.convert_to_mb(size) for _, size in files_info]

        # Calculate average and standard deviation
        avg_size_MB = round(statistics.mean(sizes_mb), 2)
        std_dev_size_MB = round(statistics.stdev(sizes_mb), 2) if len(sizes_mb) > 1 else 0.0

        # Find the file with maximum and minimum size
        max_file, max_size = max(files_info, key=lambda x: x[1])
        min_file, min_size = min(files_info, key=lambda x: x[1])

        return {
            "average_size_MB": avg_size_MB,
            "std_dev_size_MB": std_dev_size_MB,
            "max_size_file": max_file,
            "max_size_MB": Video_info.convert_to_mb(max_size),
            "min_size_file": min_file,
            "min_size_MB": Video_info.convert_to_mb(min_size)
        }

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

        # Organize all stats into a dictionary for easy consumption.
        stats = {
            "average": avg_time,                        # Average processing time (seconds)
            "std_dev": sd_time,                        # Standard deviation (seconds)
            "max_city": max_row['City'],               # City with the longest processing time
            "max_value": max_row['Video processing time (in s)'],  # Maximum time (seconds)
            "min_city": min_row['City'],               # City with the shortest processing time
            "min_value": min_row['Video processing time (in s)']   # Minimum time (seconds)
        }

        # Return the computed statistics.
        return stats

    def count_cities_by_continent(self, csv_file):
        """
        Counts how many cities are from each continent in the provided CSV file.

        Args:
            csv_file (str): Path to the CSV file.

        Returns:
            pandas.Series: Number of cities per continent.
        """
        return csv_file['Continent'].value_counts()
