from typing import List
import numpy as np
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

matrix = np.array([
[5, 2, 3, 2, 7],
[6, 8, 4, 2, 5],
[6, 4, 3, 7, 2],
[6, 9, 0, 4, 0],
[4, 1, 2, 4, 0]
])
print(row_red(matrix)[0])





