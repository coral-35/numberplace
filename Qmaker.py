import copy
import heapq
import random
import solver9x9
import printer

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

# 初期リストを作成
A_place_list = solver9x9.solve(Q_place)
printer.multi_printer(A_place_list)

while len(A_place_list) < 100:
    # 親盤面をコピー
    A_place = copy.deepcopy(A_place_list[-1])

    # ランダムに要素を削除
    del_count = 0
    while del_count < 40:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if A_place[row][col] != 0:
            A_place[row][col] = 0
            del_count += 1

    print("new Q")
    printer.single_printer(A_place)
    new_A_place_list = solver9x9.solve(A_place)
    printer.multi_printer(new_A_place_list)

    A_place_list.extend(new_A_place_list)

