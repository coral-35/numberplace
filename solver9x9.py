# 9x9ナンプレソルバー
import copy

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

# 途中チェック(枝切り)
def check(place):
    for i in range(9):
        rowset = set()
        colset = set()
        blockset = set()
        for j in range(9):
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
            block_row = i // 3 * 3 + j // 3
            block_col = i % 3 * 3 + j % 3
            if place[block_row][block_col] != 0:
                if place[block_row][block_col] in blockset:
                    return False
                blockset.add(place[block_row][block_col])
    return True

# ソルバー
def solve(place):
    for i in range(9):
        for j in range(9):
            # 空いているとき全パターン試す
            if place[i][j] == 0:
                for k in range(1, 10):
                    place[i][j] = k
                    if check(place):
                        solve(place)
                place[i][j] = 0
                return False
            
    # 全部埋まったらチェック
    if clear_check(place):
        A_place_list.append(copy.deepcopy(place))

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
for i, A_place in enumerate(A_place_list):
    print(f'Answer {i+1}')
    for row in A_place:
        print(row)