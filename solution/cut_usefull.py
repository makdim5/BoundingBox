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

dets = pd.read_csv(f'{args.path}.csv')
dets.head()

cap = cv2.VideoCapture(f'{args.path}.mkv')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def to_pixel(vector):
    return np.int16(np.round(vector * np.tile((width, height), 2)))


def get_rectangle(frame, bbox):
    return frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]


tracklets = dict()
first_frame = dict()
tracker = SimBasedTracker(30)
for frame_num in range(length):
    bboxes = tracker.update(dets[dets.frame == frame_num].values[:, 1:])
    
    for bbox in bboxes:
        bbox, id = bbox[:4], int(bbox[4])
        if id not in tracklets:
            tracklets[id] = list()
            first_frame[id] = frame_num
        tracklets[id].append(bbox)


nearest = None
min_dist = np.inf
best_tracklet = None
length_threshold = 0.8

for id, tracklet in tracklets.items():
    if len(tracklet) > length_threshold * length:
        dist = np.reshape(tracklet, (-1, 2, 2)).mean(axis=(0, 1)) - 0.5
        dist = np.linalg.norm(dist)
        if dist < min_dist:
            nearest = id
            min_dist = dist
            best_tracklet = to_pixel(tracklet)


if nearest is None:
    print('Correct car is not found')
            

aim_size = (320, 320)
low_size = (16, 16)
wait_msecs = 200
threshold = 80

last_hash = np.zeros(low_size, dtype=np.uint8)
last_i = 0


def transform_to_hash(image):
    image_hash = cv2.resize(image, low_size, interpolation=2)
    image_hash = cv2.cvtColor(image_hash, cv2.COLOR_BGR2GRAY)
    image_hash = (image_hash - image_hash.mean() > 0).astype('uint8')
    return image_hash    


if best_tracklet is not None:
    cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame[nearest])
    for i in range(len(best_tracklet)):
        code, frame = cap.read()
        if not code:
            break

        frame = get_rectangle(frame, best_tracklet[i])
        frame = cv2.resize(frame, aim_size, interpolation=2)

        frame_hash = transform_to_hash(frame)
        if i - last_i > 30:
            threshold = max(60, threshold - 5)
        
        if np.sum(frame_hash ^ last_hash) > threshold:
            if i - last_i > 10:
                threshold = max(110, threshold + 5)

            last_hash = frame_hash
            last_i = i

            cv2.imshow('check', frame)
            #cv2.imshow('hash', cv2.resize(last_hash, (256, 256), interpolation=0) * 255)
            cv2.waitKey(wait_msecs)






