size = 9
blocksize = 3
blocknum = size // blocksize

def printer(size, blocksize, place):
    blocknum = size // blocksize
    for block_i in range(blocknum):
        for i in range(blocksize):
            for block_j in range(blocknum):
                for j in range(blocksize):
                    print(place[block_i * blocksize + i][block_j * blocksize + j], end=" ")
                if block_j != blocknum - 1:
                    print("|", end=" ")
            print()
        if block_i != blocknum - 1:
            print("- - - + - - - + - - -")

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

printer(size, blocksize, Q_place)