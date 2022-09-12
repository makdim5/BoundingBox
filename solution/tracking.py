import cv2
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tracker import SimBasedTracker
from time import sleep

parser = argparse.ArgumentParser(description='Collect data for configuration')
parser.add_argument('--path')
args = parser.parse_args()

import os
dets = pd.read_csv(f'{args.path}.csv')
dets.head()

video_size = (640, 480)
cap = cv2.VideoCapture(f'{args.path}.mkv')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'h264')
video_writer = cv2.VideoWriter(f'output.mkv', fourcc, 30, video_size)


def to_pixel(vector):
    return np.int16(np.round(vector * np.tile(video_size, 2)))


def draw_rectangle(frame, bbox):
    bbox, id = to_pixel(bbox[:4]), int(bbox[4])
    center = np.int16(np.round((bbox[:2] + bbox[2:4]) / 2)) - (20, -5)
    cv2.rectangle(frame, tuple(bbox[:2]), tuple(bbox[2:4]), (255, 255, 255))
    cv2.putText(frame, f'#{id}', tuple(center), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


tracker = SimBasedTracker(30)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
for i in range(length):
    code, frame = cap.read()
    frame = cv2.resize(frame, video_size)
    
    bboxes = tracker.update(dets[dets.frame == i].values[:, 1:])
    for det in bboxes:
        draw_rectangle(frame, det)
    
    cv2.imshow('check', frame)
    cv2.waitKey(1)
    sleep(0.01)
    
    video_writer.write(frame)






