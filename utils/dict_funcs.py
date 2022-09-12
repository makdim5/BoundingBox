def unpack_coords(coords):
    return sum(coords, ())


def get_key_from_value(mydict, value):
    return list(mydict.keys())[list(mydict.values()).index(value)]


def get_list_elements_places(mylist):
    return {elem: [index for index in range(len(mylist))
                   if mylist[index] == elem] for elem in mylist}

