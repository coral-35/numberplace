import copy
import random
import solver9x9
import printer

def make_random_place():
    Q_place = [[0 for _ in range(9)] for _ in range(9)]
    for n in range(1,10):
        # 0～8の重複のない並び替えを生成
        numbers = list(range(9))
        random_i = random.sample(numbers, len(numbers)) 
        random_j = random.sample(numbers, len(numbers)) 
        # print(random_i)
        # print(random_j)
        block_set = set()
        for idx in range(9):
            i = random_i[idx]
            j = random_j[idx]
            block_row = i // 3 
            block_col = j // 3
            block_num = block_row * 3 + block_col
            if Q_place[i][j] == 0 and block_num not in block_set:
                Q_place[i][j] = n
                block_set.add(block_num)
        # printer.single_printer(Q_place)
        # print()
    return copy.deepcopy(Q_place)

def make_A_place():
    A_place = make_random_place()
    while True:
        printer.single_printer(A_place)
        print()

        # 解を求める
        solver9x9.A_place_list = []
        solver9x9.solve_recur(A_place)
        if len(solver9x9.A_place_list) > 0: # 解が見つかったら終了
            break
        else: # 数字を1つずつ減らしていく
            flg = False
            for i in range(9):
                if flg:
                    break
                for j in range(9):
                    if A_place[i][j] != 0:
                        A_place[i][j] = 0
                        flg = True
                        break
    printer.multi_printer(solver9x9.A_place_list)

if __name__ == '__main__':
    make_A_place()