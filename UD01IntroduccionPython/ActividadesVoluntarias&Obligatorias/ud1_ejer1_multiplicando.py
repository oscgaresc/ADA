##############################
# UNIDAD 1 - Ejercicio 1     #
# Multiplicando              #
##############################

#try-exception para controlar el mensaje de error en caso de no añadir un entero.
try:
     # Se solicita al usuario un número entero entre 1 y 10
    entero = int(input("Dame un número entero del 1 al 10: "))
    if entero>0 and entero<=10:
        print(f'\nTABLA DE MULTIPLICAR DEL Nº {entero}:')
        for i in range(10):
            #print(f'{entero} x {i+1} = {entero*(i+1)}')
            print('\t%2d x %2d = %2d' %(entero,i+1, entero*(i+1)))
    else:
        print(f'[31mERROR: {entero} no es un nº entero entre 1 y 10')
except ValueError:
    print("[31mError. El dato no es un entero.")
finally:
    print("\n[0mFin del programa, hasta pronto.") # reseteando el color rojo