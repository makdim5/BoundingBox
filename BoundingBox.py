import cv2
from utils.random_funcs import *
from utils.geometric_funcs import *
from utils.dict_funcs import unpack_coords


class BoundingBox:
    NAME = "Car"

    def __init__(self, current_coords):
        self.id = get_random_number()
        self.prev_coords = dict()
        self.color = get_random_color()

        self.__current_coords = current_coords

        self.is_drawing = True

    def draw(self, frame, name=NAME):
        if self.is_drawing:
            cv2.putText(frame, f"{name} {self.id}", self.__current_coords[1],
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(frame,
                          *self.__current_coords, self.color, 2)

    def update_current_coords(self, coords, frame_number):
        if coords:
            self.prev_coords[frame_number] = self.__current_coords
            self.__current_coords = coords
            self.is_drawing = True
        else:
            self.is_drawing = False

    def get_current_coords(self):
        return self.__current_coords

    def get_current_center_coords(self):
        return get_central_rect_coords(*unpack_coords(
            self.__current_coords))

    def __repr__(self):
        return str(self.id)
