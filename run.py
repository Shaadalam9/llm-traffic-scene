import common
from custom_logger import CustomLogger
from logmod import logs
from utils.yolo_detection import YOLO_detection
from utils.information import Video_info
from utils.analysis import Analysis_class
from utils.figures import Plots
from utils.frames_extractor import VideoFrameExtractor
import shutil
import os
import pandas as pd
import math

# Initialise logging with config-specified level and color output.
logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # Custom logger for standardised log messages

# Instantiate main processing classes for detection, info analysis, and general analysis.
detection = YOLO_detection()             # For YOLO object detection on videos
video_info = Video_info()                # For gathering video information/statistics
analysis = Analysis_class()              # For CSV reading and analytical calculations
plots = Plots()                          # For plotting
frame_extractor = VideoFrameExtractor()  # For frame extraction

# Load file paths and operational flags from the central config.
video_folder = common.get_configs("videos")             # Directory containing videos to process
data_path = common.get_configs("data")                  # Directory to store per-video CSV detection results
delete_runs_files = common.get_configs("delete_runs_files")  # Flag: delete YOLO 'runs' output after processing
mapping_file = common.get_configs("mapping")            # Path to the main city/country mapping CSV

# Read the main city/country mapping CSV (could include other columns like continent, region, etc.)
df_mapping = pd.read_csv(mapping_file)

# --- Run YOLO detection on input videos (if always_analyse flag is set) ---
if common.get_configs("always_analyse"):
    logger.info(f"Running YOLO on the videos present in the {video_folder}")

    # Before starting new detection runs, clear out any previous 'runs/detect' results to avoid mixups.
    folder_path = os.path.join("runs", "detect")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)   # Recursively delete the directory and all its contents

    # Only proceed if a videos directory is specified and tracking_mode is enabled in configs
    if video_folder and common.get_configs("tracking_mode"):
        for filename in os.listdir(video_folder):   # Iterate through all files in the videos directory
            # Skip hidden files and any files that don't look like common video file types
            if filename.startswith('.') or not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                continue

            full_path = os.path.join(video_folder, filename)  # Get full file path

            # Confirm it's a regular file (not a directory)
            if os.path.isfile(full_path):
                filename = os.path.basename(full_path)         # Just the filename part
                name_without_ext = os.path.splitext(filename)[0]   # Remove file extension

                # If a processed CSV already exists for this video, skip it (no need to re-run)
                if os.path.exists(os.path.join(data_path, f"{name_without_ext}.csv")):
                    logger.info(f"Processed video file already present for {name_without_ext}")
                    continue

                # Set the video title for downstream YOLO functions (used for labeling outputs)
                detection.set_video_title(name_without_ext)
                # Run YOLO in tracking mode (processes video, produces a CSV in 'runs/detect/')
                detection.tracking_mode(full_path, video_fps=25)

                # Move the newly created CSV from YOLO's default output directory to the target data directory
                new_file_path = os.path.join("runs", "detect", f"{name_without_ext}.csv")
                os.makedirs(data_path, exist_ok=True)   # Ensure data directory exists
                shutil.move(new_file_path, data_path)   # Move the CSV file to data_path

                # If enabled, clean up YOLO's output directory after each video is processed
                if delete_runs_files:
                    shutil.rmtree(os.path.join("runs", "detect"))

# --- Read all processed CSV files for analysis ---

# Use the analysis helper to read all CSV files from data_path into a dict of DataFrames.
# Key: video/country/city name; Value: DataFrame with detection results
dfs = analysis.read_csv_files(data_path)

# --- Log various high-level video statistics ---
# Each of these methods outputs summary stats (could be total videos, city-by-continent stats, etc.)
sounds = video_info.analyse_video_files(video_folder)  # Summarise input video set
video_info.count_cities_by_continent(df_mapping)  # Count how many cities are per continent
video_info.video_processing_time_stats(df_mapping)  # Analyse/Log processing times

# --- Count specific YOLO object types in each video/country ---
# Define which object types (by YOLO's class IDs) we're interested in aggregating.
target_yolo_ids = [0, 1, 2, 3, 5, 7, 9]  # Only count these YOLO class IDs

# Map YOLO class IDs to their human-readable object names
yolo_id_to_object = {
    0: "Persons",
    1: "Bicycles",
    2: "Cars",
    3: "Motorbikes",
    5: "Buses",
    7: "Trucks",
    9: "Traffic lights"
}

# For each country (or video/city), count the appearances of each object of interest.
result = {}   # Will hold final counts for each city/video
for city_country, df in dfs.items():
    parts = city_country.split("_")
    city = "_".join(parts[:-1])
    country = parts[-1]
    city_counts = {}
    for yolo_id in target_yolo_ids:
        # Get the human-readable object name, fallback to just the ID if not mapped
        object_name = yolo_id_to_object.get(yolo_id, str(yolo_id))

        # Use analysis helper to count instances of this object in the DataFrame
        count = analysis.count_object(df, yolo_id)
        city_counts[object_name] = count

        # Normalise city names in both DataFrame and input for matching
        norm_city = video_info.normalise_str(city)
        df_mapping['city_norm'] = df_mapping['City'].astype(str).map(video_info.normalise_str)

        match = df_mapping[df_mapping['city_norm'] == norm_city]

        if not match.empty:
            city_counts['iso'] = match.iloc[0]['ISO']  # If your mapping column is called 'iso'
            city_counts['country'] = match.iloc[0]['Country']  # Column 'Country'
            city_counts['continent'] = match.iloc[0]['Continent']  # Column 'Continent'
        else:
            city_counts['iso'] = None
            city_counts['country'] = None
            city_counts['continent'] = None
    result[city] = city_counts  # Store the results for this city/video

# Normalise keys in `sounds` just once, mapping them to their values
if sounds and isinstance(sounds, dict):
    normalised_sounds = {
        video_info.normalise_str(key): value
        for key, value in sounds.items()
    }
else:
    normalised_sounds = {}

for city, data in result.items():
    city_norm = video_info.normalise_str(city)
    country_norm = video_info.normalise_str(data['country'])
    key_norm = f"{city_norm}_{country_norm}"
    if key_norm in normalised_sounds and normalised_sounds[key_norm] is not None:
        result[city]['sound'] = float(normalised_sounds[key_norm])
    else:
        result[city]['sound'] = math.nan

# Print the cities where 'sound' is nan
nan_sound_cities = [city for city in result if math.isnan(result[city]['sound'])]
logger.info("Cities where the sound is not present: {nan_sound_cities}.".format(nan_sound_cities=nan_sound_cities))

# --- Update mapping file (CSV) with the new object counts ---
for city_country, values in result.items():

    city_norm = video_info.normalise_str(city)

    # Normalise all cities in the mapping dataframe (once, outside the loop is better for efficiency!)
    df_mapping['City_norm'] = df_mapping['City'].apply(video_info.normalise_str)

    # Find the row(s) in the mapping CSV where 'City' matches this city/video name
    idx = df_mapping[df_mapping['City_norm'] == city_norm].index

    if len(idx) == 0:
        logger.error(f"Warning: {city} not found in CSV.")   # Alert if the city name doesn't match any row
        continue
    idx = idx[0]  # Take the first matching row index

    # For each counted object, update the corresponding column in the DataFrame
    for key, val in values.items():
        if key in df_mapping.columns:
            df_mapping.at[idx, key] = val   # Set the cell value (overwriting old data, if any)

# --- Save the updated mapping with counts ---

# Ensure output directory exists and write the DataFrame to a new CSV file
output_dir = "_output"
os.makedirs(output_dir, exist_ok=True)
df_mapping.to_csv(os.path.join(output_dir, "mapping_updated.csv"), index=False)

plots.plot_choropleth(result,
                      value_key='sound',
                      title_text="",
                      filename="sound"
                      )

plots.stack_plot(result,
                 df_mapping,
                 order_by="alphabetical",
                 title_text="",
                 filename="stack_alphabetical",
                 font_size_captions=30,
                 legend_x=0.87,
                 legend_y=0.21,
                 legend_spacing=0.03,
                 left_margin=0,
                 right_margin=0
                 )

plots.stack_plot(result,
                 df_mapping,
                 order_by="average",
                 title_text="",
                 filename="stack_average",
                 font_size_captions=30,
                 legend_x=0.87,
                 legend_y=0.21,
                 legend_spacing=0.03,
                 left_margin=0,
                 right_margin=0
                 )

plots.stack_plot(result,
                 df_mapping,
                 order_by="continent_average",
                 title_text="",
                 filename="continent_average",
                 font_size_captions=30,
                 legend_x=0.87,
                 legend_y=0.21,
                 legend_spacing=0.03,
                 left_margin=0,
                 right_margin=0
                 )

# Run the script for frame generation
frame_extractor.process_all_videos()
