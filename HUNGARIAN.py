from cmath import inf
import numpy as np
from typing import List, Tuple
from typing import Any
from copy import deepcopy


def row_red(matrix, fi = 0):
    fi = fi
    for row in range(len(matrix)):
        minim = min(matrix[row])
        fi += minim
        for col in range(len(matrix[row])):
            matrix[row][col] -= minim 
    return matrix, fi

def col_red(matrix, fi = 0):
    matrix = np.transpose(matrix)
    fi = fi
    for row in range(len(matrix)):
        minim = min(matrix[row])
        fi += minim
        for col in range(len(matrix[row])):
            matrix[row][col] -= minim
    matrix = np.transpose(matrix)
    return matrix, fi

def reduction(matrix):
    matrix, fi = row_red(matrix)
    matrix, fi = col_red(matrix, fi)
    return matrix, fi

def unplug(matrix,ind_zeros_tab_row,ind_zeros_tab_col):
    for row in range(len(matrix)):
            for col in range(len(matrix)):
                if matrix[row][col] == 0 and row not in ind_zeros_tab_row and col not in ind_zeros_tab_col:
                    ind_zeros_tab_row.append(row)
                    ind_zeros_tab_col.append(col)
                    return matrix,ind_zeros_tab_row,ind_zeros_tab_col
                if len(ind_zeros_tab_col) == len(matrix):
                    break
    return matrix,ind_zeros_tab_row,ind_zeros_tab_col

def zeros_ind(matrix,ind_zeros_tab_row = None, ind_zeros_tab_col = None):
    if ind_zeros_tab_row == None: ind_zeros_tab_row = []
    if ind_zeros_tab_col == None: ind_zeros_tab_col = []
    prev_col = [0]
    while prev_col != ind_zeros_tab_col:
        while prev_col != ind_zeros_tab_col:
            prev_col = ind_zeros_tab_col[:]
            for row in range(len(matrix)):
                if 0 in matrix[row]:
                    counter = 0
                    temp = -1
                    for idx,i in enumerate(matrix[row]):
                        if i == 0 and idx not in ind_zeros_tab_col and row not in ind_zeros_tab_row:
                            counter += 1
                            temp = idx
                    if counter == 1:
                        ind_zeros_tab_row.append(row)
                        ind_zeros_tab_col.append(temp)
            
            for col in range(len(matrix)):
                if 0 in matrix[:,col]:
                    counter = 0
                    temp = -1
                    for idx,i in enumerate(matrix[:,col]):
                        if i == 0 and idx not in ind_zeros_tab_row and col not in ind_zeros_tab_col:
                            counter += 1
                            temp = idx
                    if counter == 1:
                        ind_zeros_tab_row.append(temp)
                        ind_zeros_tab_col.append(col)
        matrix,ind_zeros_tab_row,ind_zeros_tab_col = unplug(matrix,ind_zeros_tab_row,ind_zeros_tab_col)
    ind_zeros_tab = []
    for i in range(len(ind_zeros_tab_col)):
        ind_zeros_tab.append((ind_zeros_tab_row[i], ind_zeros_tab_col[i]))
    return ind_zeros_tab

def zeros_ind_main(M, prev = None):
    z = zeros_ind(M)
    if prev == None: return z
    if len(z) > len(prev): return z
    
    zeros = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j] == 0: zeros.append((i,j))
    for i in zeros:
        z = zeros_ind(M, [i[0]],[i[1]])
        if len(z) >= len(prev) and z!=prev: return z
    
    pass

def minimalny_zbior_lini(M : np.array, niezalezne : List[Tuple]):
    sha = M.shape[0]
    row = ['x' for i in range(sha)]
    col = [0 for i in range(sha)]
    prev_col = []
    prev_row = []
    for i in niezalezne:
        row[i[0]] = 0
    while (prev_col != col) and (prev_row != row):
        prev_col = col[:]
        prev_row = row[:]
        for idx,i in enumerate(M):
            for idx_j,j in enumerate(i):
                if M[idx,idx_j] == 0:
                    temp = True
                    for k in niezalezne:
                        if k[0] == idx and k[1] == idx_j:
                            temp = False
                    if temp:
                        if row[idx] == 'x':
                            col[idx_j] = 'x'
        for i in niezalezne:
            if col[i[1]] == 'x':
                row[i[0]] = 'x'
    return row, col

def pokrycie_update(M, row, col):
    minimum = inf
    for i_idx, i in enumerate(M):
        for j_idx,j in enumerate(i):
            if row[i_idx] == 'x' and col[j_idx] != 'x':
                minimum = min(minimum, j)
    for i_idx, i in enumerate(M):
        for j_idx,j in enumerate(i):
            if row[i_idx] == 'x' and col[j_idx] != 'x':
                M[i_idx,j_idx] -= minimum
            if row[i_idx] != 'x' and col[j_idx] == 'x':
                M[i_idx,j_idx] += minimum
    return M,minimum

def hungarian_method(M):
    t = (i for i in range(1000))
    fi = 0
    tab = None
    while True:
        
        M,temp = reduction(M)
        fi+=temp
        
        tab = zeros_ind_main(M,tab)

        if len(tab) == len(M):
            return tab, fi
        # zer niezależnych mniej niż N
        x_row,y_row = minimalny_zbior_lini(M, tab)
        M,temp = pokrycie_update(M,x_row,y_row)
        fi+=temp
        if next(t) == 500: return 1,2
        i = 0
import numpy.random
M = np.array([[5,2,3,2,7],
            [6,8,4,2,5],
            [6,4,3,7,2],
            [6,9,0,4,0],
            [4,1,2,4,0]])
M = numpy.random.random([6,6])

lst,fi = hungarian_method(M)
print(f"lista maszyn i przypisanych do nich zadań {lst} funkcja celu : {fi}")