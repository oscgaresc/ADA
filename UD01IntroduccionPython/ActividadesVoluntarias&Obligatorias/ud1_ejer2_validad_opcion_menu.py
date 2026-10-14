###############################
# UNIDAD 1 - Ejercicio 2      #
# Validar opción de menú      #
###############################

# Función que muestra un menú de opciones que el usuario debe seleccionar
def valida_opcion():
    opcion = -1
    # Bucle cíclico para evitar que salga del menú hasta que no seleccione
    # la opción correcta
    while opcion!=0:
        print('\n[0m==================================')#reseteando colores
        print('\tGAMIFICA EN EL AULA')
        print('==================================')
        print('1 - Cargar datos del fichero')
        print('2 - Imprimir datos')
        print('3 - Jugar')
        print('4 - Guardar datos')
        print('5 - Cambiar contraseña')
        print('0 - Salir')
        # bucle try-exception para controlar el mensaje de error cuando
        # el usuario no añada un entero
        try:
            opcion = int(input('Indica la opción seleccionada (0-5): '))
            #bucle condicional para seleccionar una de las opciones del menú
            if opcion == 1: 
                print(f'La opción seleccionada es: {opcion}')
            elif opcion == 2 :
                print(f'La opción seleccionada es: {opcion}')
            elif opcion == 3 :
                print(f'La opción seleccionada es: {opcion}') 
            elif opcion == 4 :
                print(f'La opción seleccionada es: {opcion}') 
            elif opcion == 5 :
                print(f'La opción seleccionada es: {opcion}')
            elif opcion == 0 :
                print(f'\nFin del programa, hasta pronto.') 
            else:
                print(f'[31mERROR: {opcion} no es un nº entero entre 0 y 5, vuelve a intentarlo.')

        except ValueError:
            print("[31mError. El dato no es un entero, vuelve a intentarlo.")
            opcion = -1
# Llamada a la función sin parámetros
valida_opcion()
        

        