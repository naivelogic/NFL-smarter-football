import cv2

def capture_video_image(youtube_video, frame_rate=5):
    image_name = youtube_video[:-4]+"_"
    vidcap = cv2.VideoCapture(youtube_video)
    
    def getFrame(sec, image_name):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite(image_name+str(count)+".jpg", image)     # save frame as JPG file
        return hasFrames

    sec = 0
    frameRate = frame_rate #5 #//it will capture image in each 5 second
    count=1
    success = getFrame(sec, image_name)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec, image_name)
    
    print("image capture completed for: ", youtube_video)
    
capture_video_image('./demo_video/dak_short.mp4', frame_rate=5)
