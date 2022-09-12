from math import fabs, sqrt


def find_rect_square(x0, y0, x1, y1):
    return fabs(x1 - x0) * fabs(y1 - y0)


def get_central_rect_coords(x0, y0, x1, y1):
    return (x1 + x0) // 2, (y1 + y0) // 2


def find_points_distance(first_point_coords, second_point_coords):
    x0, y0 = first_point_coords
    x1, y1 = second_point_coords
    return sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def is_point_in_rect_area(point_coords, rect_area):
    x0, y0, x1, y1 = rect_area
    x, y = point_coords
    return x0 <= x <= x1 and y0 <= y <= y1


def get_coords_in_simple_list(coords):
    # coords = ((x0, y0), (x1, y1))
    # returns [x0, y0, x1, y1]

    return list(sum(coords, ()))


def get_rects_intersection_area(rect1_coords, rect2_coords):
    x0, y0, x1, y1 = rect1_coords
    x0_2, y0_2, x1_2, y1_2 = rect2_coords

    left = max(x0, x0_2)
    top = min(y1, y1_2)
    right = min(x1, x1_2)
    bottom = max(y0, y0_2)

    width = right - left
    height = top - bottom

    return width * height if width * height > 0 else 0


def get_rects_union_area(rect1_coords, rect2_coords):
    return (find_rect_square(*rect1_coords) +
            find_rect_square(*rect2_coords) -
            get_rects_intersection_area(rect1_coords, rect2_coords))


def get_intersection_over_union(rect1_coords, rect2_coords):
    return (get_rects_intersection_area(rect1_coords, rect2_coords) /
            get_rects_union_area(rect1_coords, rect2_coords) if
            get_rects_union_area(rect1_coords, rect2_coords) else
            0)
