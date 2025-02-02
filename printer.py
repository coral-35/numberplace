def single_printer(place):
    size = len(place)
    blocksize = int(size ** 0.5)
    blocksize = int(size ** 0.5)
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
            separator = ""
            for i in range(size):
                separator += "- " if (i + 1) % blocksize != 0 else "- + "
            separator = separator.rstrip(" + ")  # 最後の "+ " を削除
            print(separator)

def multi_printer(places):
    for i, place in enumerate(places):
        print(f'Answer {i+1}')
        single_printer(place)
        print()

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
    multi_printer([Q_place])