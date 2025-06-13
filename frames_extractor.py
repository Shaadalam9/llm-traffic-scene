# Extract the first frame of the video
import cv2
import os
import common
from custom_logger import CustomLogger
from logmod import logs

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger

# Set your input video folder path and output snaps folder path
input_folder = common.get_configs("videos")
output_folder = common.get_configs("snaps")

# Supported video file extensions
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(video_extensions):
        video_path = os.path.join(input_folder, filename)
        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        if success:
            snap_name = os.path.splitext(filename)[0] + ".png"
            snap_path = os.path.join(output_folder, snap_name)
            cv2.imwrite(snap_path, frame)
            print(f"Saved first frame of {filename} as {snap_name}")
        else:
            print(f"Could not read {filename}")
        cap.release()
