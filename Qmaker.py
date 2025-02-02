import solver9x9
import printer

def make_random_place():

    # # ランダムに穴を開ける
    # import random
    # for i in range(9):
    #     for j in range(9):
    #         if random.randint(0, 1) == 0:
    #             A_place[i][j] = 0

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

    return Q_place

def make_A_place():
    while True:
        solver9x9.A_place_list = []
        A_place = make_random_place()
        solver9x9.solve(A_place)
        if len(solver9x9.A_place_list) > 0:
            break

    printer.multi_printer(solver9x9.A_place_list)