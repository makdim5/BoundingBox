import numpy as np
from scipy.optimize import linear_sum_assignment


def calculate_intersection(bb_test, bb_gt):
    bb_test = bb_test.reshape(-1, 4)
    bb_gt = bb_gt.reshape(-1, 4)
    x1 = np.maximum(bb_test[:, 0], bb_gt[:, 0])
    y1 = np.maximum(bb_test[:, 1], bb_gt[:, 1])
    x2 = np.minimum(bb_test[:, 2], bb_gt[:, 2])
    y2 = np.minimum(bb_test[:, 3], bb_gt[:, 3])
    width = np.maximum(0., x2 - x1)
    height = np.maximum(0., y2 - y1)
    intersection = width * height

    return bb_test, bb_gt, intersection


def get_bbox_area(bboxes):
    return (bboxes[:, 2] - bboxes[:, 0]) * (bboxes[:, 3] - bboxes[:, 1])
    # faster then np.prod(bboxes[:, 2:] - bboxes[:, :2], axis=1)


def compute_intersection_over_bb(bb_test, bb_gt):
    """
    Computes IoU between two bboxes in the form [x1,y1,x2,y2]
    """
    bb_test, bb_gt, intersection = calculate_intersection(bb_test, bb_gt)
    union = get_bbox_area(bb_test) + get_bbox_area(bb_gt) - intersection
    return intersection / union


class TrackingObj:

    def __init__(self, id, bbox):
        self.id = id
        self.bbox = bbox
        self.alpha = 0.4
        self.not_updated = 0

    def similarity(self, other):
        score = compute_intersection_over_bb(self.bbox, other.bbox)
        return score

    def update(self, other):
        self.not_updated = 0
        self.bbox = self.alpha * self.bbox + (1 - self.alpha) * other.bbox
        
    def update_age(self):
        self.not_updated += 1

    def to_row(self):
        row = np.zeros(5)
        row[:4] = self.bbox
        row[4] = self.id
        return row.reshape(1, -1)


class SimBasedTracker:
    def __init__(self, keep_history=30, sim_threshold=0.07):
        self.last_id = 0
        self.id2obj = dict()
        self.keep_history = keep_history
        self.sim_threshold = sim_threshold

    def get_bboxes(self):
        bboxes = [box.to_row() for box in self.id2obj.values() if box.not_updated == 0]

        if not bboxes:
            return np.zeros((0, 5))
        return np.vstack(bboxes)

    def update(self, bboxes):
        """
            bboxes are np.ndarray (N, 4), where row is (x0, y0, x1, y1)
        """
        bboxes = np.array(bboxes).reshape(-1, 4)
        if len(self.id2obj) == 0:
            for bbox in bboxes:
                obj = TrackingObj(self.last_id, bbox)
                self.id2obj[self.last_id] = obj
                self.last_id += 1
        else:
            history_objects = [x for x in self.id2obj.values()]
            M_H = len(history_objects)
            M_W = bboxes.shape[0]
            sim_matrix = np.zeros((M_H, M_W))
            new_objects = [TrackingObj(-1, bbox) for bbox in bboxes]

            for i, hist_obj in enumerate(history_objects):
                for j, new_obj in enumerate(new_objects):
                    sim_matrix[i, j] = hist_obj.similarity(new_obj)

            sim_matrix = np.nan_to_num(sim_matrix)
            rows, cols = linear_sum_assignment(sim_matrix, maximize=True)
            to_keep = np.where(sim_matrix[rows, cols] > self.sim_threshold)
            rows = rows[to_keep]
            cols = cols[to_keep]

            unused_old = set(range(M_H))
            unused_new = set(range(M_W))
            for i in range(len(rows)):
                row = rows[i]
                col = cols[i]
                history_objects[row].update(new_objects[col])
                unused_old.remove(row)
                unused_new.remove(col)

            for old in unused_old:
                history_objects[old].update_age()

            if unused_new:
                objs = [obj.bbox for obj in self.id2obj.values()]
                objs = np.array(objs)

                for new in unused_new:
                    obj = TrackingObj(self.last_id, bboxes[new])
                    self.id2obj[self.last_id] = obj
                    self.last_id += 1

            to_del = []
            for idx, old_obj in self.id2obj.items():
                if old_obj.not_updated > self.keep_history:
                    to_del.append(idx)
            for idx in to_del:
                del self.id2obj[idx]
        return self.get_bboxes()

