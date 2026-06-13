from camera import Camera
import cv2

def main():
    print("initializing camera")
    cam = Camera()
    print("camera initialized")
    # cam.show_frame()
    # cam.stream()
    cam.stream_skin()

if __name__ == "__main__":
    main()