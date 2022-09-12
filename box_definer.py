def define_popular_box_id(boxes):
    popular_box = boxes[0]

    for box in boxes:
        if len(box.prev_coords) > len(popular_box.prev_coords):
            popular_box = box

    return popular_box.id
