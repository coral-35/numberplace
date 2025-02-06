import copy
import os
import pandas
import random
import solver9x9
import solver9x9_recur
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
solve_flg, A_place_list = solver9x9.solve(Q_place)

list_idx = 0
# csv から ID を取得
try:
    idlist = pandas.read_csv("placeid_list" + str(list_idx) + ".csv")["id"].tolist()
    idset = set(idlist)
    print(idset)
except:
    idset = set()

print(len(idset), "loaded")

idset.add(place_ID_changer.place_to_id(Q_place))
get_id_count = 0
while get_id_count < 100000:
    # 親盤面をコピー
    Q_place = copy.deepcopy(A_place_list[-1])

    # ランダムに要素を削除
    del_count = [1 if Q_place[i][j] == 0 else 0 for j in range(9) for i in range(9)].count(1)
    while del_count < 30:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if Q_place[row][col] != 0:
            Q_place[row][col] = 0
            del_count += 1

    # print("new Q")
    # printer.single_printer(Q_place)
    new_A_place_list = solver9x9_recur.solve(Q_place)
    # printer.multi_printer(new_A_place_list)

    for new_A_place in new_A_place_list:
        id = place_ID_changer.place_to_id(new_A_place)
        idset.add(id)
        get_id_count += 1

    # print("idset", len(idset))
    # print()

    # csv に書き込み
    placeid_list = list(idset)
    csv_path = os.path.join(os.path.dirname(__file__), "placeid_list" + str(list_idx) + ".csv")
    pandas.DataFrame(placeid_list, columns=["id"]).to_csv(csv_path, index=False)
    if len(placeid_list) > 10000:
        list_idx += 1
        idset = set()

placeid_list = list(idset)
firstid = placeid_list[0]
lastid = placeid_list[-1]
print(firstid)
print(lastid)
issame = [1 if firstid[i] == lastid[i] else 0 for i in range(len(firstid))]
print(sum(issame))