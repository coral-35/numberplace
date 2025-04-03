import copy
import os
import random
import pandas
import numberplace.printer as printer
import numberplace.place_ID_changer as place_ID_changer

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
def check_point(place, i, j):
    for k in range(9):
        if place[i][k] == place[i][j] and k != j:
            return False
        if place[k][j] == place[i][j] and k != i:
            return False
    for k in range(3):
        for l in range(3):
            if place[i//3*3+k][j//3*3+l] == place[i][j] and (i//3*3+k != i or j//3*3+l != j):
                return False
    return True

# 重複なし盤面作成
def make_A_place():
    place = [[0 for i in range(9)] for j in range(9)]
    place[0] = random.sample(range(1, 10), 9) 
    # printer.single_printer(place)
    stack = []
    stack.append(place)
    # 深さ優先探索
    while stack:
        place = stack.pop()
        # print("pop")
        # printer.single_printer(place)
        chg_flg = False
        for i in range(9):
            for j in range(9):
                if place[i][j] == 0:
                    chg_flg = True
                    for k in range(1, 10):
                        place[i][j] = k
                        # printer.single_printer(place)
                        if check_point(place, i, j):
                            stack.append(copy.deepcopy(place))
                if chg_flg:
                    break
            if chg_flg:
                break
        if clear_check(place):
            return place

# 重複なし盤面リスト作成
def make_A_placeid_list(num):
    A_place_list = []
    for i in range(num):
        A_place_list.append(place_ID_changer.place_to_id(make_A_place()))
    csv_path = os.path.join(os.path.dirname(__file__), "A_placeid_list.csv")
    pandas.DataFrame(A_place_list, columns=["id"]).to_csv(csv_path, index=False)

if __name__ == "__main__":
    A_list_idx = 0
    list_size = 10000
    Aplaceid_list = []
    try:
        while True:
            csv_path = os.path.join(os.path.dirname(__file__), "A_placeid_list_" + str(A_list_idx) + ".csv")
            if os.path.exists(csv_path):
                Aplaceid_list = pandas.read_csv(csv_path)["id"].tolist()
                if  len(Aplaceid_list) < list_size:
                    break
            else:
                break
            A_list_idx += 1
    except:
        pass
    
    while True:
        Aplaceid_list.append(place_ID_changer.place_to_id(make_A_place()))
        csv_path = os.path.join(os.path.dirname(__file__), "A_placeid_list_" + str(A_list_idx) + ".csv")
        pandas.DataFrame(Aplaceid_list, columns=["id"]).to_csv(csv_path, index=False)
        if len(Aplaceid_list) >= list_size:
            A_list_idx += 1
            Aplaceid_list = []
        if A_list_idx > 100:
            break
        