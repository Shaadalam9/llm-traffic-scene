# by Shadab Alam <md_shadab_alam@outlook.com>
import math
import os
import shutil

import pandas as pd

import common
from custom_logger import CustomLogger
from logmod import logs
from utils.analysis import Analysis_class
from utils.figures import Plots
from utils.information import Video_info


# Initialise logging with config-specified level and colour output.
logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)

# Instantiate the CSV processing helpers once. Video specific helpers are
# imported lazily only when a fresh video analysis is requested.
video_info = Video_info()
analysis = Analysis_class()
plots = Plots()

# Load shared file paths and operational flags from the central config.
video_folder = common.get_configs("videos")
data_path = common.get_configs("data")
delete_runs_files = common.get_configs("delete_runs_files")
always_analyse = common.get_configs("always_analyse")

REPEATED_MAPPING_FILENAME = "mapping-10.csv"
REPEATED_DATA_FOLDERNAME = "10_data"
REPEATED_VIDEO_FOLDERNAME = "10_videos"


def get_mapping_files(configured_mapping):
    """Return an ordered list of mapping files configured for this run.

    ``mapping`` may be either a single path or a list of paths. For backwards
    compatibility, a single ``mapping.csv`` setting also includes a sibling
    ``mapping-10.csv`` file when it is present.
    """
    if isinstance(configured_mapping, str):
        mapping_files = [configured_mapping]

        mapping_directory = os.path.dirname(configured_mapping)
        mapping_filename = os.path.basename(configured_mapping)
        mapping_10_file = os.path.join(mapping_directory, "mapping-10.csv")
        if mapping_filename == "mapping.csv" and os.path.exists(mapping_10_file):
            mapping_files.append(mapping_10_file)
    elif isinstance(configured_mapping, (list, tuple)):
        mapping_files = list(configured_mapping)
    else:
        raise TypeError("The 'mapping' config value must be a path or a list of paths.")

    unique_mapping_files = []
    for mapping_file in mapping_files:
        if not isinstance(mapping_file, str) or not mapping_file.strip():
            raise ValueError("Every mapping entry must be a non-empty path string.")
        if mapping_file not in unique_mapping_files:
            unique_mapping_files.append(mapping_file)

    return unique_mapping_files


def get_mapping_source_folders(mapping_file):
    """Return the detection and video folders assigned to a mapping file."""
    if os.path.basename(mapping_file) == REPEATED_MAPPING_FILENAME:
        return (
            os.path.join(data_path, REPEATED_DATA_FOLDERNAME),
            os.path.join(video_folder, REPEATED_VIDEO_FOLDERNAME)
        )
    return data_path, video_folder


def list_video_files(folder_path, recursive=False):
    """List supported video files from one source folder."""
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    if not os.path.isdir(folder_path):
        return []

    if not recursive:
        return [
            os.path.join(folder_path, filename)
            for filename in os.listdir(folder_path)
            if not filename.startswith('.')
            and filename.lower().endswith(video_extensions)
            and os.path.isfile(os.path.join(folder_path, filename))
        ]

    video_files = []
    for current_folder, folders, filenames in os.walk(folder_path):
        folders[:] = [folder for folder in folders if not folder.startswith('.')]
        for filename in filenames:
            if filename.lower().endswith(video_extensions):
                video_files.append(os.path.join(current_folder, filename))
    return video_files


def run_detection(mapping_files):
    """Run YOLO once for all videos that do not already have a result CSV."""
    if not always_analyse:
        return

    from utils.yolo_detection import YOLO_detection

    detection = YOLO_detection()

    logger.info(f"Running YOLO on the videos present in {video_folder}.")

    folder_path = os.path.join("runs", "detect")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    if not video_folder or not common.get_configs("tracking_mode"):
        return

    for mapping_file in mapping_files:
        mapping_data_folder, mapping_video_folder = get_mapping_source_folders(mapping_file)
        recursive = os.path.basename(mapping_file) == REPEATED_MAPPING_FILENAME
        for full_path in list_video_files(mapping_video_folder, recursive=recursive):
            name_without_ext = os.path.splitext(os.path.basename(full_path))[0]
            processed_file = os.path.join(mapping_data_folder, f"{name_without_ext}.csv")
            if os.path.exists(processed_file):
                logger.info(f"Processed video file already present for {name_without_ext}")
                continue

            detection.set_video_title(name_without_ext)
            detection.tracking_mode(full_path, video_fps=25)

            new_file_path = os.path.join("runs", "detect", f"{name_without_ext}.csv")
            os.makedirs(mapping_data_folder, exist_ok=True)
            shutil.move(new_file_path, mapping_data_folder)

            if delete_runs_files:
                shutil.rmtree(os.path.join("runs", "detect"))


def get_city_from_result_name(city_country):
    """Extract the city portion from a ``City_Country`` result filename."""
    if "_" not in city_country:
        return city_country
    return city_country.rsplit("_", 1)[0]


def normalise_result_key(value):
    """Normalise filename separators and punctuation for reliable matching."""
    normalised = video_info.normalise_str(value)
    if not isinstance(normalised, str):
        return normalised
    return ''.join(character for character in normalised if character.isalnum())


def analyse_mapping(mapping_file, dfs, normalised_sounds, mapping_data_folder):
    """Analyse matching detection results and create outputs for one mapping."""
    logger.info(f"Processing mapping file {mapping_file}.")
    df_mapping = pd.read_csv(mapping_file)
    df_mapping['city_norm'] = df_mapping['City'].astype(str).map(video_info.normalise_str)
    df_mapping['result_key'] = (
        df_mapping['City'].astype(str) + df_mapping['Country'].astype(str)
    ).map(normalise_result_key)

    video_info.count_cities_by_continent(df_mapping)
    video_info.video_processing_time_stats(df_mapping)

    target_yolo_ids = [0, 1, 2, 3, 5, 7, 9]
    yolo_id_to_object = {
        0: "Persons",
        1: "Bicycles",
        2: "Cars",
        3: "Motorbikes",
        5: "Buses",
        7: "Trucks",
        9: "Traffic lights"
    }

    result = {}
    for city_country, df in dfs.items():
        city = get_city_from_result_name(city_country)
        city_norm = video_info.normalise_str(city)
        result_key = normalise_result_key(city_country)
        match = df_mapping[df_mapping['result_key'] == result_key]

        # Retain compatibility with the original City_Country filename parser.
        if match.empty:
            match = df_mapping[df_mapping['city_norm'] == city_norm]

        # A shared data directory can contain results belonging to the other
        # mapping. Only analyse rows represented by the current mapping file.
        if match.empty:
            continue

        mapping_row = match.iloc[0]
        city = str(mapping_row['City'])
        city_counts = {
            yolo_id_to_object[yolo_id]: analysis.count_object(df, yolo_id)
            for yolo_id in target_yolo_ids
        }
        city_counts['iso'] = mapping_row['ISO']
        city_counts['country'] = mapping_row['Country']
        city_counts['continent'] = mapping_row['Continent']

        sound = normalised_sounds.get(result_key)
        if sound is not None:
            city_counts['sound'] = float(sound)
        elif 'sound' in mapping_row.index and pd.notna(mapping_row['sound']):
            # Existing CSV mode does not inspect the videos. Retain a sound
            # value that has already been saved in the mapping file.
            city_counts['sound'] = float(mapping_row['sound'])
        else:
            city_counts['sound'] = math.nan
        result[city] = city_counts

    logger.info(
        "Matched {} of {} mapping rows in {} to detection CSV files.",
        len(result),
        len(df_mapping),
        mapping_file
    )
    matched_city_names = {video_info.normalise_str(city) for city in result}
    unmatched_city_names = [
        city
        for city in df_mapping['City'].astype(str)
        if video_info.normalise_str(city) not in matched_city_names
    ]
    if unmatched_city_names:
        logger.warning(
            "Mapping rows without detection CSV data in {}: {}.",
            mapping_file,
            unmatched_city_names
        )
    if not result:
        logger.error(
            "No detection CSV files matched {}. Ensure its files are present "
            "somewhere under {} and use City_Country filenames.",
            mapping_file,
            mapping_data_folder
        )

    nan_sound_cities = [city for city, values in result.items() if math.isnan(values['sound'])]
    logger.info(
        "Cities where the sound is not present for {}: {}.",
        mapping_file,
        nan_sound_cities
    )

    for city, values in result.items():
        city_norm = video_info.normalise_str(city)
        indices = df_mapping[df_mapping['city_norm'] == city_norm].index
        if len(indices) == 0:
            logger.error(f"Warning: {city} not found in {mapping_file}.")
            continue

        index = indices[0]
        for key, value in values.items():
            target_column = key
            if key == "Bicycles" and key not in df_mapping.columns and "Cycles" in df_mapping.columns:
                target_column = "Cycles"
            if target_column in df_mapping.columns:
                df_mapping.at[index, target_column] = value

    output_dir = "_output"
    os.makedirs(output_dir, exist_ok=True)
    mapping_stem = os.path.splitext(os.path.basename(mapping_file))[0]
    output_file = os.path.join(output_dir, f"{mapping_stem}_updated.csv")
    df_mapping.drop(columns=['city_norm', 'result_key']).to_csv(output_file, index=False)
    logger.info(f"Saved updated mapping to {output_file}.")

    if not result:
        logger.warning(f"Skipping figures for {mapping_file} because no detection data matched.")
        return

    mapping_name = os.path.basename(mapping_file)
    if mapping_name == "mapping.csv":
        plots.plot_choropleth(
            result,
            value_key='sound',
            title_text="",
            filename="sound"
        )
        plots.stack_plot(
            result,
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
        plots.stack_plot(
            result,
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
        plots.stack_plot(
            result,
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
    elif mapping_name == "mapping-10.csv":
        plots.plot_city_stacked_bars(
            df_mapping,
            title_text="",
            filename="bar_plot",
            font_size_captions=20,
            legend_x=0.02,
            legend_y=0.97,
            left_margin=0,
            right_margin=0
        )


def main():
    mapping_files = get_mapping_files(common.get_configs("mapping"))
    missing_mapping_files = [mapping_file for mapping_file in mapping_files if not os.path.isfile(mapping_file)]
    if missing_mapping_files:
        raise FileNotFoundError(f"Mapping files not found: {missing_mapping_files}")

    run_detection(mapping_files)

    if not always_analyse:
        logger.info(
            "Using existing detection CSV files and analysing video audio; "
            "skipping YOLO and video metadata."
        )

    for mapping_file in mapping_files:
        mapping_data_folder, mapping_video_folder = get_mapping_source_folders(mapping_file)
        recursive = os.path.basename(mapping_file) == REPEATED_MAPPING_FILENAME

        logger.info(
            "Using detection folder {} and video folder {} for {}.",
            mapping_data_folder,
            mapping_video_folder,
            mapping_file
        )

        dfs = analysis.read_csv_files(mapping_data_folder, recursive=recursive)
        sounds = video_info.analyse_video_files(
            mapping_video_folder,
            inspect_metadata=always_analyse,
            recursive=recursive
        ) or {}
        normalised_sounds = {
            normalise_result_key(key): value
            for key, value in sounds.items()
        }
        analyse_mapping(mapping_file, dfs, normalised_sounds, mapping_data_folder)

    if always_analyse:
        from utils.frames_extractor import VideoFrameExtractor

        frame_extractor = VideoFrameExtractor()
        frame_extractor.process_all_videos()


if __name__ == "__main__":
    main()
