import cv2 as cv
import numpy as np
from cv2.typing import MatLike

class Camera:

    def __init__(self, camera_index=0):
        self.cam = cv.VideoCapture(camera_index, cv.CAP_DSHOW)
        if not self.cam.isOpened():
            print("Cannot open camera")
            exit()
        self.width = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            return None
        return frame
    
    def show_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            print("capture failed")
            return
        cv.imshow("Camera Frame", frame)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def stream(self):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("capture failed")
                break
            b,g,r = cv.split(frame)
            black = np.zeros_like(b)
            b = cv.merge((b, black, black))
            g = cv.merge((black, g, black))
            r = cv.merge((black, black, r))
            
            # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # ret, thres = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
            lower = np.array([127, 127, 127])
            upper = np.array([180, 180, 180])
            thres = cv.inRange(frame, lower, upper)
            # r = frame[:,:,2]
            # g = frame[:,:,1]
            # b = frame[:,:,0]

            cv.imshow("Camera Stream - Threshold", thres)
            cv.imshow("Camera Stream - Red Channel", r)
            cv.imshow("Camera Stream - Green Channel", g)
            cv.imshow("Camera Stream - Blue Channel", b)
            # cv.imshow("Camera Stream", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cam.release()
        cv.destroyAllWindows()
    
    def stream_skin(self):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("capture failed")
                break
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            ycbcr = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)

            lower_hsv = np.array([0, 58, 0])
            upper_hsv = np.array([35, 174, 255])

            skin = cv.inRange(hsv, lower_hsv, upper_hsv)

            cv.imshow("Camera Stream - Skin Detection", skin)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cam.release()
        cv.destroyAllWindows()

    def get_skin(self) -> MatLike:
        ret, frame = self.cam.read()
        if not ret:
            print("capture failed")
            raise RuntimeError("Failed to capture frame from camera")
        frame = cv.fastNlMeansDenoisingColored(frame, None, 0, 5)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        ycbcr = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)

        lower_hsv = np.array([0, 58, 0])
        upper_hsv = np.array([35, 174, 255])

        skin = cv.inRange(hsv, lower_hsv, upper_hsv)
        return skin

    def release(self):
        self.cam.release()