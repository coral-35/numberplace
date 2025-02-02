def place_to_id(place):
    return "".join([str(i) for row in place for i in row])

def id_to_place(id):
    size = int(len(id) ** 0.5)
    return [[int(id[i*size+j]) for j in range(size)] for i in range(size)]

if __name__ == '__main__':
    Q_place = [
        [1, 8, 0, 9, 6, 0, 7, 4, 0],
        [0, 0, 6, 0, 8, 0, 5, 2, 1],
        [0, 4, 2, 0, 5, 0, 0, 9, 8],
        [2, 7, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 9, 0, 7, 3, 0, 8, 0],
        [3, 6, 0, 8, 2, 0, 0, 7, 5],
        [6, 0, 3, 0, 0, 8, 2, 1, 4],
        [0, 2, 7, 0, 0, 5, 0, 3, 6],
        [4, 9, 0, 0, 0, 0, 0, 0, 0]
    ]
    id = place_to_id(Q_place)
    print(id)
    place = id_to_place(id)
    print(place)
