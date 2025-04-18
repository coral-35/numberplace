# 4x4ナンプレソルバー
import copy
import numberplace.printer as printer

# クリアチェック
def clear_check(place):
    for i in range(4):
        rowset = set(place[i])
        if len(rowset) != 4 or 0 in rowset:
            return False
        colset = set([place[j][i] for j in range(4)])
        if len(colset) != 4 or 0 in colset:
            return False
        blockset = set([place[i//2*2+j//2][i%2*2+j%2] for j in range(4)])
        if len(blockset) != 4 or 0 in blockset:
            return False
    return True

# 途中チェック(枝切り)
def check(place):
    for i in range(4):
        rowset = set()
        colset = set()
        blockset = set()
        for j in range(4):
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
            block_row = i // 2 * 2 + j // 2
            block_col = i % 2 * 2 + j % 2
            if place[block_row][block_col] != 0:
                if place[block_row][block_col] in blockset:
                    return False
                blockset.add(place[block_row][block_col])
    return True

# ソルバー
def solve_recur(place, solutions):
    for i in range(4):
        for j in range(4):
            # 空いているとき全パターン試す
            if place[i][j] == 0:
                for k in range(1, 5):
                    place[i][j] = k
                    if check(place):
                        solve_recur(place, solutions)
                place[i][j] = 0
                return False
            
    # 全部埋まったらチェック
    if clear_check(place):
        solutions.append(copy.deepcopy(place))
    return True

def solve(place):
    solutions = []
    solve_recur(place, solutions)
    return solutions

if __name__ == '__main__':
    Q_place = [
        [1, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 1, 0, 0],
        [2, 0, 0, 0]
    ]
    A_place_list = solve(Q_place)
    printer.multi_printer(A_place_list)