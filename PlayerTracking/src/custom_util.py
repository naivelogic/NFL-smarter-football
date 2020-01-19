# labels
from object_detection.utils import label_map_util

def load_label_map(LABEL_PATH, NUM_CLASSES):
    """
    LOAD LABEL MAP
    """
    try:
        label_map = label_map_util.load_labelmap(LABEL_PATH)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
    except:
        import traceback
        traceback.print_exc()
    return category_index

def capture_single_video(index=0, duration=5, fps=30, output_dir="out/captured_videos",
                         filetype="mp4"):
    """
    Ramps up camera provided by index and captures video for provided capture_duration (in sec).
    """
    camera_feed = CameraFeed(index)
    camera_feed.ramp(fps)
    filepath = create_filepath(output_dir, filetype)

    writer = None

    start_time = time.time()
    while time.time() < start_time + duration:
        frame = camera_feed.get_next(True, False)
        if writer is None:
            (height, width) = frame.shape[:2]
            writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*"MP4V"),
                                     fps, (width, height))
        writer.write(frame)

    writer.release()
    camera_feed.close()

    TextFormatter.print_info("Video was captured for %s seconds." % duration) 