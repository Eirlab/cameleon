from cv2 import cv2

def find_camera():
    # Find availables cameras
    camera_list = []
    for i in range(0, 10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(i)
                cap.release()
        except:
            pass
    return camera_list

def display_camera_stream(camera_list):
    for i in camera_list:
        cap = cv2.VideoCapture(i)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

print(find_camera())
display_camera_stream(find_camera())