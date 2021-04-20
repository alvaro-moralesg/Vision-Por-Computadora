# Crear una funcion 'adivinar' que permita adiviniar
# un numero generado de forma aleatoria 

import random

def adivinar(intentos):
	x = random.randint(0,100)
	#print (x)
	for i in range(0, intentos):
		print ('Intento Nº',i+1 ,': ', end = '')
		num = int(input())
		if num == x :
			print ('Felicidades. Adivino el numero en', i, 'intentos.')
			exit()
		else :
			print ('Numero incorrecto.', end = '')
	else :
		print ('\nHa superado el numero de intentos. Suerte para la proxima.')
		exit()

print ('Adivine el numero generado de forma aleatoria entre 0 y 100.')
intentos = int (input ('Primero ingrese la cantidad de intentos: '))
print ('Comencemos')
adivinar(intentos)