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

A_place_list = []
solver9x9.solve_recur(Q_place)
printer.single_printer(A_place_list[0])