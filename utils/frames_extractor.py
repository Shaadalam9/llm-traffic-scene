import cv2
import os
import common
from custom_logger import CustomLogger
from logmod import logs


class VideoFrameExtractor:
    def __init__(self):
        # Initialise logging and config
        logs(show_level=common.get_configs("logger_level"), show_color=True)
        self.logger = CustomLogger(__name__)
        self.input_folder = common.get_configs("videos")
        self.output_folder = common.get_configs("snaps")
        self.video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
        self._create_output_folder()

    def _create_output_folder(self):
        """Create the output folder if it doesn't exist."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            self.logger.info(f"Created output folder: {self.output_folder}")

    def extract_first_frame(self, filename):
        """Extract and save the first frame of a given video file."""
        video_path = os.path.join(self.input_folder, filename)
        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        if success:
            snap_name = os.path.splitext(filename)[0] + ".png"
            snap_path = os.path.join(self.output_folder, snap_name)
            cv2.imwrite(snap_path, frame)
            self.logger.info(f"Saved first frame of {filename} as {snap_name}")
        else:
            self.logger.error(f"Could not read {filename}")
        cap.release()

    def process_all_videos(self):
        """Process all supported video files in the input folder."""
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(self.video_extensions):
                self.extract_first_frame(filename)


if __name__ == "__main__":
    extractor = VideoFrameExtractor()
    extractor.process_all_videos()
