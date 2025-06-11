import common
from custom_logger import CustomLogger
from logmod import logs
from tqdm import tqdm
import os
import pandas as pd

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger


class Analysis_class:
    def __init__(self) -> None:
        pass

    def read_csv_files(self, folder_path):
        """
        Reads all CSV files in the specified folders, processes them if configured,
        and returns their contents as a dictionary keyed by file name.

        This function will:
          - For each folder, it will check if it exists and log a warning if not.
          - For each CSV file found, it will read the file into a pandas DataFrame.
          - Optionally apply geometry correction to the DataFrame if enabled in the configuration.
          - Look up additional values using the provided mapping and the file's base name.
          - Adds the DataFrame to the results only if:
                - The mapping values exist and the population of the city is greater than the
                    configured `footage_threshold,
                - The total seconds are greater than the configured `footage_threshold`.

        Args:
            folder_paths (list[str]): List of folder paths containing the CSV files.
            df_mapping (Any): A mapping object used to find values related to each file (for example, video IDs).

        Returns:
            dict: Dictionary where keys are the base file names (without extension),
                  and values are the corresponding pandas DataFrames of each CSV file.
                  Only files meeting all value requirements are included.
        """
        dfs = {}
        logger.info("Reading csv files.")

        if not os.path.exists(folder_path):
            logger.warning(f"Folder does not exist: {folder_path}.")

        for file in tqdm(os.listdir(folder_path)):
            if file.endswith(".csv"):
                filename = os.path.splitext(file)[0]

                file_path = os.path.join(folder_path, file)
                try:
                    logger.debug(f"Adding file {file_path} to dfs.")

                    # Read the CSV into a DataFrame
                    df = pd.read_csv(file_path)

                    # Add the DataFrame to the dict
                    dfs[filename] = df
                except Exception as e:
                    logger.error(f"Failed to read {file_path}: {e}.")
                    continue  # Skip to the next file if reading fails
        return dfs

    def count_object(self, dataframe, id):
        """
        Counts the number of unique instances of an object with a specific ID in a DataFrame.

        Args:
            dataframe (DataFrame): The DataFrame containing object data.
            id (int): The unique ID assigned to the object.

        Returns:
            int: The number of unique instances of the object with the specified ID.
        """

        # Filter the DataFrame to include only entries for the specified object ID
        crossed_ids = dataframe[(dataframe["YOLO_id"] == id)]

        # Group the filtered data by Unique ID
        crossed_ids_grouped = crossed_ids.groupby("Unique Id")

        # Count the number of groups, which represents the number of unique instances of the object
        num_groups = crossed_ids_grouped.ngroups

        return num_groups
