"""
Video demo for showing live object detection from a camera / video feed

python main.py
"""

import cv2
import time
import numpy as np

from pipeline import DetectAndTrack


class VideoDemo():
    def __init__(self,
                 #pipeline,
                 camera = 1,
                 width = 640,
                 height = 480,
                 fps = 8.0,
                 record = False,
                 filename="./media/outputs/demo_output.mp4"):
        self.camera = camera
        #self.pipeline = pipeline
        self.width = width
        self.height = height
        self.fps = fps
        self.record = record
        self.filename = filename
        self.videowriter = None
        self.initialize()

    def initialize(self):

        
        self.capture = cv2.VideoCapture(self.camera)
        if not self.capture.isOpened():
            print("Error opening video camera")
            return

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if self.record:
            self.videowriter = cv2.VideoWriter(self.filename,
                                                cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                                self.fps,
                                                (self.width, self.height), 
                                                isColor=True)

    def start(self):
        
        # Create instances for object detection
        detect_and_track = DetectAndTrack(min_conf=0.3, max_age=2, min_hits=1)

        while(True):

            start_time = time.time()
            ret, img = self.capture.read()

            #filename = "temp.jpg"
            #cv2.imwrite(filename, image)
            #img = skimage.img_as_float(imread(filename))

            np.asarray(img)
            new_img = detect_and_track.pipeline(img)
            
            # Write out frame to video    
            if self.videowriter is not None:
                if self.videowriter.isOpened():
                    self.videowriter.write(new_img)     #  , audio=False
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()
        end = time.time()
        print(round(end - start, 2), 'Seconds to finish')
    


if __name__ == "__main__":
    #Constants
    CAMERA = "../media/demo_videos/dak_demo.mp4"
    SAVED_VIDEO = False
    SAVED_VIDEO_FILE_NAME = "../media/outputs/demo_output.mp4"

    videodemo = VideoDemo(camera = CAMERA, 
                          record=SAVED_VIDEO,
                          filename=SAVED_VIDEO_FILE_NAME)
    # https://github.com/STU-Idichi-Syoya/tensor-RTforJetson-nano/blob/4365776037308978f36a1f3d4594e6676ba3ae0b/tf_trt_models/utils/camera.py#L119
    # Threading for jetson                      

    #detector = ObjectDetector()
    #detect_and_track = DetectAndTrack(min_conf=0.3, max_age=2, min_hits=2)
    videodemo.start()       # ask the camera to start grabbing images