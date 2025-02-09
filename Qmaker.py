import copy
import os
import pandas
import random
import solver9x9
import printer
import place_ID_changer

def make_X_place():
    Q_place = [[0 for i in range(9)] for j in range(9)]
    for i in range(4):
        for j in range(5):
            r = random.randint(1, 11)
            if r <= 2: 
                Q_place[i][j] = "X"
                Q_place[8-j][i] = "X"
                Q_place[j][8-i] = "X"
                Q_place[8-i][8-j] = "X"
    r = random.randint(1, 11)
    if r <= 2: # 30%
        Q_place[4][4] = "X"
    return Q_place

def make_Q_place(X_place, A_place):
    Q_place = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            if X_place[i][j] == "X":
                Q_place[i][j] = A_place[i][j]
    return Q_place

try_num = 0
Qplaceid_list = []
Aplaceid_list = []

# 初期問題を読み込む
csv_path = os.path.join(os.path.dirname(__file__), "Q_A_placeid_list.csv")
if os.path.exists(csv_path):
    df = pandas.read_csv(csv_path)
    Qplaceid_list = df["Q_id"].tolist()
    Aplaceid_list = df["A_id"].tolist()
    
# while try_num < 10000:
while True:
    # X 盤面を作成
    X_place = make_X_place()
    # print("X_place")
    # printer.single_printer(X_place)
    
    # 重複のない解答盤面を選択
    list_idx = 0
    A_list = pandas.read_csv("A_placeid_list_0.csv")["id"].tolist()
    r = random.randint(0, len(A_list)-1)
    # print("r:", r)
    A_place = place_ID_changer.id_to_place(A_list[r])

    # 問題盤面を作成
    Q_place = make_Q_place(X_place, A_place)
    # print("Q_place")
    # printer.single_printer(Q_place)

    solve_flg, A_place_list = solver9x9.solve(copy.deepcopy(Q_place))
    if solve_flg:
        # printer.multi_printer(A_place_list)
        if len(A_place_list) == 1:
            # print("unique")
            Qplaceid_list.append(place_ID_changer.place_to_id(Q_place))
            Aplaceid_list.append(place_ID_changer.place_to_id(A_place))
            csv_path = os.path.join(os.path.dirname(__file__), "Q_A_placeid_list.csv")
            df = pandas.DataFrame({"Q_id": Qplaceid_list, "A_id": Aplaceid_list})
            df.to_csv(csv_path, index=False)
            if df.shape[0] == 10000:
                break
    else:
        pass
        # print("no solution, A_place_X")
        # printer.single_printer(Q_place)

    try_num += 1
