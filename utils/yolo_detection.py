# by Shadab Alam <md_shadab_alam@outlook.com>
from ultralytics import YOLO
import os
import common
from custom_logger import CustomLogger
from logmod import logs
from tqdm import tqdm
import cv2
from collections import defaultdict
import shutil
import numpy as np
import pandas as pd

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger

display_frame_tracking = common.get_configs("display_frame_tracking")
confidence = common.get_configs("confidence")
save_annoted_img = common.get_configs("save_annoted_img")
save_tracked_img = common.get_configs("save_tracked_img")
delete_labels = common.get_configs("delete_labels")
delete_frames = common.get_configs("delete_frames")

# Consts
LINE_TICKNESS = 1
RENDER = False
SHOW_LABELS = False
SHOW_CONF = False


class YOLO_detection:
    def __init__(self, video_title=None):
        """
        Initialises a new instance of the class.

        Parameters:
            video_title (str, optional): The title of the video. Defaults to None.

        Instance Variables:
            self.model (str): The model configuration loaded from common.get_configs("model").
            self.resolution (str): The video resolution. Initialized as None and set later when needed.
            self.video_title (str): The title of the video.
        """
        self.model = common.get_configs("model")
        self.resolution = None
        self.video_title = video_title

    def set_video_title(self, title):
        """
        Sets the video title for the instance.

        Parameters:
            title (str): The new title for the video.
        """
        self.video_title = title

    def tracking_mode(self, input_video_path, video_fps=25):
        """
        Performs object tracking on a video using YOLO and saves tracking results.

        Parameters:
            input_video_path (str): Path to the input video.
            output_video_path (str): Path to save the final output video.
            video_fps (int, optional): Frames per second for the output video (default is 25).

        This function processes each frame:
            - Runs YOLO tracking.
            - Saves annotated frames and tracking data.
            - Optionally displays the annotated video.
            - Appends tracking labels to a CSV file.
        """
        model = YOLO(self.model)
        cap = cv2.VideoCapture(input_video_path)

        # Store the track history
        track_history = defaultdict(lambda: [])

        # Output paths for frames, txt files, and final video
        frames_output_path = os.path.join("runs", "detect", "frames")
        annotated_frame_output_path = os.path.join("runs", "detect", "annotated_frames")
        tracked_frame_output_path = os.path.join("runs", "detect", "tracked_frame")
        txt_output_path = os.path.join("runs", "detect", "labels")
        text_filename = os.path.join("runs", "detect", "track", "labels", "image0.txt")
        display_video_output_path = os.path.join("runs", "detect", "display_video.mp4")

        # Create directories if they don't exist
        os.makedirs(frames_output_path, exist_ok=True)
        os.makedirs(txt_output_path, exist_ok=True)
        os.makedirs(annotated_frame_output_path, exist_ok=True)
        os.makedirs(tracked_frame_output_path, exist_ok=True)

        # Initialise a VideoWriter for the final video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore

        if display_frame_tracking:
            display_video_writer = cv2.VideoWriter(display_video_output_path,
                                                   fourcc, video_fps, (int(cap.get(3)), int(cap.get(4))))

        # Open video and get total frames
        cap = cv2.VideoCapture(input_video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            print("Warning: Could not determine total frames. Progress bar may not work correctly.")
            total_frames = None  # Prevent tqdm from setting a fixed length

        # Setup progress bar
        progress_bar = tqdm(total=total_frames, unit="frames", dynamic_ncols=True)

        # Loop through the video frames
        frame_count = 0  # Variable to track the frame number
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:

                frame_count += 1  # Increment frame count

                # Run YOLO tracking on the frame, persisting tracks between frames
                results = model.track(frame,
                                      tracker='bytetrack.yaml',
                                      persist=True,
                                      conf=confidence,
                                      save=True,
                                      save_txt=True,
                                      line_width=LINE_TICKNESS,
                                      show_labels=SHOW_LABELS,
                                      show_conf=SHOW_CONF,
                                      show=RENDER,
                                      verbose=False)

                # Update progress bar
                progress_bar.update(1)

                # Get the boxes and track IDs
                boxes = results[0].boxes.xywh.cpu()  # type: ignore
                if boxes.size(0) == 0:
                    with open(text_filename, 'w') as file:   # noqa: F841
                        pass

                try:
                    track_ids = results[0].boxes.id.int().cpu().tolist()  # type: ignore

                    # Visualise the results on the frame
                    annotated_frame = results[0].plot()

                # Save annotated frame to file
                    if save_annoted_img:
                        frame_filename = os.path.join(annotated_frame_output_path, f"frame_{frame_count}.jpg")
                        cv2.imwrite(frame_filename, annotated_frame)

                except Exception:
                    pass

                # Save txt file with bounding box information
                with open(text_filename, 'r') as text_file:
                    data = text_file.read()
                new_txt_file_name = os.path.join("runs", "detect", "labels", f"label_{frame_count}.txt")
                with open(new_txt_file_name, 'w') as new_file:
                    new_file.write(data)

                labels_path = os.path.join("runs", "detect", "labels")
                output_csv_path = os.path.join("runs", "detect", f"{self.video_title}.csv")

                YOLO_detection.merge_txt_to_csv_dynamically(labels_path, output_csv_path, frame_count)

                os.remove(text_filename)
                if delete_labels is True:
                    os.remove(os.path.join("runs", "detect", "labels", f"label_{frame_count}.txt"))

                # save the labelled image
                if delete_frames is False:
                    image_filename = os.path.join("runs", "detect", "track", "image0.jpg")
                    new_img_file_name = os.path.join("runs", "detect", "frames", f"frame_{frame_count}.jpg")
                    shutil.move(image_filename, new_img_file_name)

                # Plot the tracks
                try:
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point
                        if len(track) > 30:  # retain 90 tracks for 90 frames
                            track.pop(0)

                        # Draw the tracking lines
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230),
                                      thickness=LINE_TICKNESS*5)

                except Exception:
                    pass

                # Display the annotated frame
                if display_frame_tracking:
                    cv2.imshow("YOLOv11 Tracking", annotated_frame)
                    display_video_writer.write(annotated_frame)

                # Save the annotated frame here
                if save_tracked_img:
                    frame_filename = os.path.join(tracked_frame_output_path, f"frame_tracked_{frame_count}.jpg")
                    cv2.imwrite(frame_filename, annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()
        progress_bar.close()

    @staticmethod
    def merge_txt_to_csv_dynamically(txt_location, output_csv, frame_count):
        """
        Merges YOLO-format label data from a .txt file into a CSV, frame by frame.

        Parameters:
            txt_location (str): Directory containing label .txt files.
            output_csv (str): Path to the CSV file to update.
            frame_count (int): Frame number being processed (used for naming).
        """
        # Define the path for the new text file
        new_txt_file_name = os.path.join(txt_location, f"label_{frame_count}.txt")

        # Read data from the new text file
        with open(new_txt_file_name, 'r') as text_file:
            data = text_file.read()

        # Save the data into the new text file
        with open(new_txt_file_name, 'w') as new_file:
            new_file.write(data)

        # Read the newly created text file into a DataFrame
        df = pd.read_csv(new_txt_file_name, delimiter=" ", header=None,
                         names=["YOLO_id", "X-center", "Y-center", "Width", "Height", "Unique Id"])
        df['Frame Count'] = frame_count

        # Append the DataFrame to the CSV file
        if not os.path.exists(output_csv):
            df.to_csv(output_csv, index=False, mode='w')  # If the CSV does not exist, create it
        else:
            df.to_csv(output_csv, index=False, mode='a', header=False)  # If it exists, append without header
