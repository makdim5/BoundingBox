import time

import cv2

from box_definer import define_popular_box_id
from tracking import track_boxes
from utils.csv_utils import get_coords_per_frame_number

FRAME_DATA_PATH = "media\\test_video_1.csv"
VIDEO_PATH = 'media\\test_video_1.mkv'

RESOLUTION = 416


# task one
def define_boxes_throw_the_video(boxes, frame, frame_number):
    frame_height, frame_width = frame.shape[:2]
    coords_per_frame = get_coords_per_frame_number(
        frame_number, FRAME_DATA_PATH,
        frame_height, frame_width)

    track_boxes(boxes, coords_per_frame, frame_number)

    for bound_box in boxes:
        bound_box.draw(frame)


# task two
def write_video_in_resolution(video_writer, boxes, car_id, frame, frame_number):
    box_for_writing = boxes[0]
    for box in boxes:
        if box.id == car_id:
            box_for_writing = box
            break

    if frame_number in box_for_writing.prev_coords.keys():
        x0, y0 = box_for_writing.prev_coords[frame_number][0]
        x1, y1 = box_for_writing.prev_coords[frame_number][1]

        video_writer.write(cv2.resize(frame[y0:y1, x0:x1], (RESOLUTION, RESOLUTION),
                                      interpolation=cv2.INTER_CUBIC))


def perform_video_frame_by_frame(action, *action_args,
                                 video_path=VIDEO_PATH, is_show=False):
    cap = cv2.VideoCapture(video_path)

    frame_number = 0

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(frame, f"{frame_number}", (0, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

        action(*action_args, frame, frame_number)

        cv2.putText(frame, f"{frame_number}", (0, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

        if is_show:
            cv2.imshow("", frame)

        # # setting hot-key "r" to play-pause video
        # if cv2.waitKey(25) == ord('r'):
        #     while True:
        #         if cv2.waitKey(25) == ord('r'):
        #             break

        # setting hot-key "Q" to finish application
        if cv2.waitKey(25) == ord('q'):
            break
        frame_number += 1

    cap.release()
    cv2.destroyAllWindows()


def main():
    boxes = []

    perform_video_frame_by_frame(define_boxes_throw_the_video,
                                 boxes, is_show=True)

    # car_id = define_popular_box_id(boxes)
    #
    # cap = cv2.VideoCapture(VIDEO_PATH)
    # video_writer = cv2.VideoWriter(f"{car_id}.mkv",
    #                                int(cv2.VideoWriter_fourcc(*'XVID')),
    #                                int(cap.get(cv2.CAP_PROP_FPS)),
    #                                (RESOLUTION, RESOLUTION))
    #
    # print("Video saving started... ")
    # perform_video_frame_by_frame(write_video_in_resolution, video_writer,
    #                              boxes, car_id)
    #
    # cap.release()
    # video_writer.release()
    # print("Video has been saved!")


if __name__ == "__main__":
    main()
