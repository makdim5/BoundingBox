import pandas as pd


def get_rect_coords(row, file, frame_height, frame_width):
    row = int(row)
    xl = pd.read_csv(file)
    return ((int(xl.at[row, "x0"] * frame_width), int(xl.at[row, "y0"] * frame_height)),
            (int(xl.at[row, "x1"] * frame_width), int(xl.at[row, "y1"] * frame_height)))


def get_coords_per_frame_number(frame_number, file, frame_height, frame_width):
    coords = []
    xl = pd.read_csv(file)
    for i in range(xl.index.stop):
        if xl.at[i, "frame"] == frame_number:
            coords.append(get_rect_coords(i, file, frame_height, frame_width))

        if xl.at[i, "frame"] > frame_number:
            break

    return coords
