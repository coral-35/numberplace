import copy
import numberplace.printer as printer

# クリアチェック
def clear_check(place):
    size = len(place)
    block_size = int(size ** 0.5)
    for i in range(size):
        rowset = set(place[i])
        if len(rowset) != size or 0 in rowset:
            return False
        colset = set([place[j][i] for j in range(size)])
        if len(colset) != size or 0 in colset:
            return False
        blockset = set([place[i//block_size*block_size+j//block_size][i%block_size*block_size+j%block_size] for j in range(size)])
        if len(blockset) != size or 0 in blockset:
            return False
    return True

# 可能性を管理する配列を初期化
def init_possib_place(place):
    size = len(place)
    possib_place = [[[True for _ in range(size)] for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if place[i][j] != 0:
                update_possib_place(place, possib_place, i, j)
    return possib_place

# 可能性を更新
def update_possib_place(place, possib_place, i, j):  
    size = len(place)
    block_size = int(size ** 0.5)
    num = place[i][j] - 1
    for k in range(size):
        possib_place[i][j][k] = False
        possib_place[i][k][num] = False
        possib_place[k][j][num] = False
    block_row = i // block_size * block_size
    block_col = j // block_size * block_size
    for r in range(block_size):
        for c in range(block_size):
            possib_place[block_row + r][block_col + c][num] = False
    possib_place[i][j][num] = True


# 一通りに定まるマスを埋める
def fill_single_possib_place(place, possib_place):
    size = len(place)
    filled = True
    while filled:
        filled = False
        for i in range(size):
            for j in range(size):
                if place[i][j] == 0:
                    possible_values = [k for k in range(size) if possib_place[i][j][k]]
                    if len(possible_values) == 1:
                        place[i][j] = possible_values[0] + 1
                        update_possib_place(place, possib_place, i, j)
                        filled = True

# ソルバー
def solve(place):
    solutions = []
    possib_place = init_possib_place(place)
    fill_single_possib_place(place, possib_place)
    if clear_check(place):
        solutions.append(copy.deepcopy(place))
    else:
        printer.single_printer(place)
        return False, place
    return True, solutions


if __name__ == '__main__':
    Q_place = [
        [1, 8, 0, 9, 6, 0, 7, 4, 0],
        [0, 0, 6, 0, 8, 0, 5, 2, 1],
        [0, 4, 2, 0, 5, 0, 0, 9, 8],
        [2, 7, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 9, 0, 7, 3, 0, 8, 0],
        [3, 6, 0, 8, 2, 0, 0, 7, 5],
        [6, 0, 3, 0, 0, 8, 2, 1, 4],
        [0, 2, 7, 0, 0, 5, 0, 3, 0],
        [4, 9, 0, 0, 0, 0, 0, 0, 0]
    ]
    solve_flg, A_place_list = solve(Q_place)
    if solve_flg:
        printer.multi_printer(A_place_list)