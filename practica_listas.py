## Practica de listas
# Crear la siguiente lista
#   2   2   5   6
#   0   3   7   4
#   8   8   5   2
#   1   5   6   1
#
# Seleccionar el subarray [8 8 5 2]
# Poner la diagonal de la matriz en cero
# Sumar todos los elementos del array
# Setear los valores pares en 0 y los impares en 1

import numpy as np

num_lst = [[2, 2, 5, 6], [0, 3, 7, 4], [8, 8, 5, 2], [1, 5, 6, 1]]
print ('Subarray seleccionado: ', num_lst[2])

num_lst_d = num_lst
for i in range(0,4):
    num_lst_d[i][i] = 0
print ('Lista con diagonal en 0: ', num_lst_d)

suma = 0
for i in range(0,4):
    for j in range (0,4):
        suma = suma + num_lst[i][j]
print('La suma de todos los elementos del array es: ', suma)

num_lst_ip = np.zeros(np.array(num_lst).shape)
# for i in range(0,4):
#     for j in range (0,4):
#         num_lst_ip[i][j] = 1 & (num_lst[i][j] % 2 == 1)
num_lst_ip[np.array(num_lst) % 2 == 1] = 1
print('Array con 0 y 1 segun si el elemento es par o impar: ',(num_lst_ip.tolist()))