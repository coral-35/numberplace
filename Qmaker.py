import copy
import heapq
import pandas
import random
import solver9x9_recur as solver9x9_recur
import printer
import place_ID_changer

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
A_place_list = solver9x9_recur.solve(Q_place)
# 親盤面をコピー
A_place = A_place_list[0]
idset = set()
idset.add(place_ID_changer.place_to_id(A_place))

while len(idset) < 100000:
    # ランダムに要素を削除
    del_count = 0
    while del_count < 50:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if A_place[row][col] != 0:
            A_place[row][col] = 0
            del_count += 1

    print("new Q")
    printer.single_printer(A_place)
    new_A_place_list = solver9x9_recur.solve(A_place)
    printer.multi_printer(new_A_place_list)

    for new_A_place in new_A_place_list:
        id = place_ID_changer.place_to_id(new_A_place)
        idset.add(id)

    A_place = new_A_place_list[-1]
    print(len(idset))

    # csv に書き込み
    placeid_list = list(idset)
    pandas.DataFrame(placeid_list).to_csv("placeid_list.csv")


placeid_list = list(idset)
firstid = placeid_list[0]
lastid = placeid_list[-1]
print(firstid)
print(lastid)
issame = [1 if firstid[i] == lastid[i] else 0 for i in range(len(firstid))]
print(sum(issame))