import numpy as np
from typing import List, Tuple
def minimalny_zbior_lini(M : np.array, niezalezne : List[Tuple]):
    sha = M.shape[0]
    row = ['x' for i in range(sha)]
    col = [0 for i in range(sha)]
    prev_col = []
    prev_row = []
    while (prev_col != col) and (prev_row != row):
        prev_col = col
        prev_row = row
        for i in niezalezne:
            row[i[0]] = 0
        zalezne = []
        for i in M:
            for j in i:
                if (i,j) not in niezalezne:
                    zalezne.append((i,j))
                    if row[i[0]] == 'x':
                        col[i[1]] = 'x'
        for i in niezalezne:
            if col[i[1]] == 'x':
                row[i[0]] = 'x'
    return row, col
