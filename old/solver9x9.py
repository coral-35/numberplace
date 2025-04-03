import copy
import numberplace.printer as printer

# クリアチェック
def clear_check(place):
    for i in range(9):
        rowset = set(place[i])
        if len(rowset) != 9 or 0 in rowset:
            return False
        colset = set([place[j][i] for j in range(9)])
        if len(colset) != 9 or 0 in colset:
            return False
        blockset = set([place[i//3*3+j//3][i%3*3+j%3] for j in range(9)])
        if len(blockset) != 9 or 0 in blockset:
            return False
    return True

# 可能性を管理する配列を初期化
def init_possib_place(place):
    possib_place = [[[True for _ in range(9)] for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if place[i][j] != 0:
                update_possib_place(place, possib_place, i, j)
    return possib_place

# 可能性を更新
def update_possib_place(place, possib_place, i, j):  
    num = place[i][j] - 1
    for k in range(9):
        possib_place[i][j][k] = False
        possib_place[i][k][num] = False
        possib_place[k][j][num] = False
    block_row = i // 3 * 3
    block_col = j // 3 * 3
    for r in range(3):
        for c in range(3):
            possib_place[block_row + r][block_col + c][num] = False
    possib_place[i][j][num] = True


# 一通りに定まるマスを埋める
def fill_single_possib_place(place, possib_place):
    filled = True
    while filled:
        filled = False
        for i in range(9):
            for j in range(9):
                if place[i][j] == 0:
                    possible_values = [k for k in range(9) if possib_place[i][j][k]]
                    if len(possible_values) == 1:
                        place[i][j] = possible_values[0] + 1
                        update_possib_place(place, possib_place, i, j)
                        filled = True
                    # あるマスで詰みが発覚したらその時点で終了
                    elif len(possible_values) == 0:
                        print("詰みました")
                        return False

# ソルバー
def solve(place):
    solutions = []
    possib_place = init_possib_place(place)
    fill_single_possib_place(place, possib_place)
    if clear_check(place):
        solutions.append(copy.deepcopy(place))
    else:
        # printer.single_printer(place)
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
    else:
        print("解けませんでした")