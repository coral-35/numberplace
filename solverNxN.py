# NxNナンプレソルバー
import copy
import printer

# クリアチェック
def clear_check(place):
    for i in range(size):
        rowset = set(place[i])
        if len(rowset) != size or 0 in rowset:
            return False
        colset = set([place[j][i] for j in range(size)])
        if len(colset) != size or 0 in colset:
            return False
        blockset = set([place[i//blocksize*blocksize+j//blocksize][i%blocksize*blocksize+j%blocksize] for j in range(size)])
        if len(blockset) != size or 0 in blockset:
            return False
    return True

# 途中チェック(枝切り)
def check(place):
    for i in range(size):
        rowset = set()
        colset = set()
        blockset = set()
        for j in range(size):
            # 行のチェック
            if place[i][j] != 0:
                if place[i][j] in rowset:
                    return False
                rowset.add(place[i][j])
            # 列のチェック
            if place[j][i] != 0:
                if place[j][i] in colset:
                    return False
                colset.add(place[j][i])
            # ブロックのチェック
            block_row = i // blocksize * blocksize + j // blocksize
            block_col = i % blocksize * blocksize + j % blocksize
            if place[block_row][block_col] != 0:
                if place[block_row][block_col] in blockset:
                    return False
                blockset.add(place[block_row][block_col])
    return True

# ソルバー
def solve(place):
    for i in range(size):
        for j in range(size):
            # 空いているとき全パターン試す
            if place[i][j] == 0:
                for k in range(1, size + 1):
                    place[i][j] = k
                    if check(place):
                        solve(place)
                place[i][j] = 0
                return False
    if clear_check(place):
        A_place_list.append(copy.deepcopy(place))

if __name__ == '__main__':
    size = 9
    blocksize = 3
    # 初期化
    A_place_list = []

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

    A_place_list = []
    solve(Q_place)
    printer.multi_printer(A_place_list)