import common
from custom_logger import CustomLogger
from logmod import logs
from utils.yolo_detection import YOLO_detection

logs(show_level=common.get_configs("logger_level"), show_color=True)
logger = CustomLogger(__name__)  # use custom logger

detection = YOLO_detection()

while True:
    video_paths = common.get_configs("videos")  # folders with videos
