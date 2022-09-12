import cv2
from utils.csv_utils import *

COLORS = [(255, 0, 0), (96, 225, 0), (248, 250, 0), (86, 250, 141), (86, 79, 141), (130, 220, 227)]
FILEPATH = "media\\test_video_1.csv"

car_id = 2

cap = cv2.VideoCapture('media\\test_video_1.mkv')

if not cap.isOpened():
    print("Error opening video  file")

frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), \
                            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_number = 0

while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        coords = get_coords_per_frame_number(frame_number,
                                             FILEPATH,
                                             frame_height,
                                             frame_width)
        if car_id < len(coords):
            cv2.rectangle(frame,
                          *coords[car_id],
                          COLORS[car_id % len(COLORS)], 2)
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        frame_number += 1
        # Press Q on keyboard to exit
        if cv2.waitKey(25) == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
