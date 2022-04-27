from typing import Any
import numpy as np

def zeros_ind(matrix):
    ind_zeros_tab_row = []
    ind_zeros_tab_col = []
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if matrix[row][col] == 0 and row not in ind_zeros_tab_row and col not in ind_zeros_tab_col:
                ind_zeros_tab_row.append(row)
                ind_zeros_tab_col.append(col)
            if len(ind_zeros_tab_col) == len(matrix):
                break
    ind_zeros_tab = []
    for i in range(len(ind_zeros_tab_col)):
        ind_zeros_tab.append((ind_zeros_tab_row[i], ind_zeros_tab_col[i]))
    return ind_zeros_tab

lst = [(0,0), (1,2),(2,4)]
if (Any,4) in lst:
    print("essa")
