from cmath import inf
import numpy as np
from typing import List, Tuple

def row_red(matrix, fi = 0):
    for row in range(len(matrix)):
        minim = min(matrix[row])
        fi += minim
        for col in range(len(matrix[row])):
            matrix[row][col] -= minim 
    return matrix, fi

def col_red(matrix, fi = 0):
    matrix = np.transpose(matrix)
    for row in range(len(matrix)):
        minim = min(matrix[row])
        fi += minim
        for col in range(len(matrix[row])):
            matrix[row][col] -= minim
    matrix = np.transpose(matrix)
    return matrix, fi

def reduction(matrix):
    # w każdym wierszu macierzy A odejmujemy najmniejszy element wiersza i tworzymy nową macierz:
    matrix, fi = row_red(matrix)
    # W każdej kolumnie macierzy A odnajdujemy najmniejszy element kolumny i tworzymy nową macierz:
    matrix, fi = col_red(matrix, fi)
    return matrix, fi

def unplug(matrix,ind_zeros_tab_row,ind_zeros_tab_col):
    # wybierz i dodaj do listy pierwsze zeero które może być niezależne
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
    # definicja list zer niezależnych
    if ind_zeros_tab_row == None: ind_zeros_tab_row = []
    if ind_zeros_tab_col == None: ind_zeros_tab_col = []
    # definicja poprzedniej wartości zer niezależnych (potrzebne do wykrywania zmian)
    prev_col = [0]
    # do czasy aż nie będzie zmiany w listach zer niezależnych:
    while prev_col != ind_zeros_tab_col:
        # do czasy aż nie będzie zmiany w listach zer niezależnych:
        while prev_col != ind_zeros_tab_col:
            prev_col = ind_zeros_tab_col[:]
            # dla każdego wiersza:
            for row in range(len(matrix)):
                # jeżeli istnieje zero w wierszu:
                if 0 in matrix[row]:
                    counter = 0
                    temp = -1
                    # jeżeli w wierszu istnieje tylko jedno zero które może zostać zerem niezależnym, dodaj to zero do listy zer niezależnych
                    for idx,i in enumerate(matrix[row]):
                        if i == 0 and idx not in ind_zeros_tab_col and row not in ind_zeros_tab_row:
                            counter += 1
                            temp = idx
                    if counter == 1:
                        ind_zeros_tab_row.append(row)
                        ind_zeros_tab_col.append(temp)
            # dla każdej kolumny:
            for col in range(len(matrix)):
                # jeżeli istnieje zero w kolumnie:
                if 0 in matrix[:,col]:
                    counter = 0
                    temp = -1
                    # jeżeli w kolumnie istnieje tylko jedno zero które może zostać zerem niezależnym, dodaj to zero do listy zer niezależnych
                    for idx,i in enumerate(matrix[:,col]):
                        if i == 0 and idx not in ind_zeros_tab_row and col not in ind_zeros_tab_col:
                            counter += 1
                            temp = idx
                    if counter == 1:
                        ind_zeros_tab_row.append(temp)
                        ind_zeros_tab_col.append(col)
        # istnieją zera niezależne które mogą zostać wpisane na wiele sposobów
        # dodaj jedno z nich do rozwiązania i kontynuuj algorytm
        matrix,ind_zeros_tab_row,ind_zeros_tab_col = unplug(matrix,ind_zeros_tab_row,ind_zeros_tab_col)
    # scal listę koordynatów zer niezależnych i ja zwróć
    ind_zeros_tab = []
    for i in range(len(ind_zeros_tab_col)):
        ind_zeros_tab.append((ind_zeros_tab_row[i], ind_zeros_tab_col[i]))
    return ind_zeros_tab

def zeros_ind_main(M, prev = None):
    # sprawdzenie czy zwrócona lista zer niezależnych jest większa od poprzedniej
    z = zeros_ind(M)
    if prev == None: return z
    if len(z) > len(prev): return z
    
    # jeżeli nie jest to po koleii zmiana parametrów wejściowych (dodanie konkretnej wartości do rozwiązania wymuszając zmianę):
    # znalezienie zer macierzy:
    zeros = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j] == 0: zeros.append((i,j))
    # wywoływanie funkcji z każdym z zer
    for i in zeros:
        z = zeros_ind(M, [i[0]],[i[1]])
        if len(z) >= len(prev) and z!=prev: return z
    
    pass

def minimalny_zbior_lini(M : np.array, niezalezne : List[Tuple]):
    # poszukiwanie maksymalnego skojarzenia:
    # definicja zmiennych:
    sha = M.shape[0]
    row = ['x' for i in range(sha)]
    col = [0 for i in range(sha)]
    prev_col = []
    prev_row = []
    # Oznaczyć symbolem x każdy wiersz nie posiadający niezależnego zera 0*
    for i in niezalezne:
        row[i[0]] = 0
    # Pętle należy kontynuować tak długo, aż nie jest możliwe dalsze oznakowanie.
    while (prev_col != col) and (prev_row != row):
        prev_col = col[:]
        prev_row = row[:]
        # Oznaczyć symbolem x każda kolumnę mającą zero zależne 0’ =(przekreślone 0) w oznaczonym wierszu
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
        # Oznaczyć symbolem x każdy wiersz mający w oznakowanej kolumnie niezależne zero 0*
        for i in niezalezne:
            if col[i[1]] == 'x':
                row[i[0]] = 'x'
    return row, col

def pokrycie_update(M, row, col):
    # znadź najmniejszy nieprzykryty przez linie element macierzy M
    minimum = inf
    for i_idx, i in enumerate(M):
        for j_idx,j in enumerate(i):
            if row[i_idx] == 'x' and col[j_idx] != 'x':
                minimum = min(minimum, j)
    # Odejmij ten element od wszystkich, nie przykrytych liniami elementów M.
    # oraz
    # Dodaj element najmniejszy do elementów macierzy M, które są przykryte dwoma liniami
    for i_idx, i in enumerate(M):
        for j_idx,j in enumerate(i):
            if row[i_idx] == 'x' and col[j_idx] != 'x':
                M[i_idx,j_idx] -= minimum
            if row[i_idx] != 'x' and col[j_idx] == 'x':
                M[i_idx,j_idx] += minimum
    # zwróć uaktualnioną macierz i minimum
    return M,minimum

def hungarian_method(M):
    # definicja zmiennych pomocniczych
    fi = 0
    tab = None
    while True:
        # krok przygotowawczy
        M,temp = reduction(M)
        # Krok 1: aktualizacja dolnego ograniczenia funkcji celu
        fi+=temp
        # Krok 2: wyznaczenie zer niezależnych
        tab = zeros_ind_main(M,tab)
        # Krok 3: jeżeli liczba zer niezależnych = N
        if len(tab) == len(M):
            return tab, fi
        # zer niezależnych mniej niż N:
        # wyznaczenie oznaczeń x na kolumnach i rzędach (potrzebnych do pokrycia liniami)
        x_row,y_row = minimalny_zbior_lini(M, tab)
        # Krok 4: próba powiększenia zbioru zer niezależnych
        M,temp = pokrycie_update(M,x_row,y_row)
        # Zwiększ wartość fi o krotność elementu minimalnego i przejdź do kroku 2
        fi+=temp

import numpy.random
M = np.array([[5,2,3,2,7],
            [6,8,4,2,5],
            [6,4,3,7,2],
            [6,9,0,4,0],
            [4,1,2,4,0]])
M = numpy.random.random([6,6])

lst,fi = hungarian_method(M)
print(f"lista maszyn i przypisanych do nich zadań {lst} funkcja celu : {fi}")