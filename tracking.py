from BoundingBox import BoundingBox
from utils.dict_funcs import unpack_coords, get_key_from_value, get_list_elements_places
from utils.geometric_funcs import get_intersection_over_union


def track_boxes(boxes, frame_coords, frame_number):
    if frame_number == 0:
        for coords in frame_coords:
            boxes.append(BoundingBox(coords))
        return

    frame_coords_and_boxes_matches = clear_frame_coords_and_boxes_matches(
        [get_suitable_box_to_one_frame_coords(one_frame_coords, boxes)
         for one_frame_coords in frame_coords
         ],
        frame_coords)

    for box in boxes:
        box.is_drawing = False

    for box, frame_coords_index in frame_coords_and_boxes_matches.items():
        if box is not None:
            box.update_current_coords(frame_coords[frame_coords_index[0]], frame_number)

    # it's possible to comment 31-35 code strings to check program with 4 boxes
    if len(frame_coords) > len(boxes):
        for i in range(len(frame_coords)):
            occured_indexes = [item[0] for item in frame_coords_and_boxes_matches.values()]
            if i not in occured_indexes:
                boxes.append(BoundingBox(frame_coords[i]))
                break

    print(frame_number,
          frame_coords_and_boxes_matches, len(frame_coords),
          f"len box: {len(boxes)}")


def clear_frame_coords_and_boxes_matches(matches, frame_coords):
    # collection -> {box: [list of frame_coords_indexes], ...}
    boxes_with_frame_coords_indexes = get_list_elements_places(matches)

    for box in boxes_with_frame_coords_indexes.keys():
        current_coords_indexes_to_box = boxes_with_frame_coords_indexes[box]

        if len(current_coords_indexes_to_box) > 1 and box is not None:
            best_coords_index = current_coords_indexes_to_box[0]

            for coords_index in current_coords_indexes_to_box:
                first_degree = get_matching_degree(box, frame_coords[coords_index])
                second_degree = get_matching_degree(
                    box, frame_coords[best_coords_index])

                if compare_degrees(first_degree, second_degree):
                    best_coords_index = coords_index

            boxes_with_frame_coords_indexes[box] = [best_coords_index]

    return boxes_with_frame_coords_indexes


def get_suitable_box_to_one_frame_coords(one_frame_coords, boxes):
    degrees = {
        box_index:
            get_matching_degree(box, one_frame_coords)
        for box_index, box in enumerate(boxes)
    }

    suitable_degree = list(degrees.values())[0]

    for degree in degrees.values():
        if compare_degrees(degree, suitable_degree):
            suitable_degree = degree

    suitable_box = boxes[get_key_from_value(degrees, suitable_degree)]

    return suitable_box


def compare_degrees(first_degree, second_degree):
    intersection1 = first_degree

    intersection2 = second_degree

    comparison = intersection1 > intersection2

    return comparison


def get_matching_degree(box, one_frame_coords, iou_threshold=0.45):
    intersection_over_union = get_intersection_over_union(
        unpack_coords(box.get_current_coords()),
        unpack_coords(one_frame_coords))

    # if intersection_over_union < iou_threshold:
    #     intersection_over_union = 0

    return intersection_over_union
