###############################
# UNIDAD 1 - Ejercicio 4      #
# Diccionario vuelo           #
###############################

vuelo = {'origen':'Valencia', 'destino':'Menorca', 'día':'15-08', 'clase':'turista'}
acaba = False
while not acaba:
    #Mostramos el menú y solicitamos la operación al usuario
    opciones_validas = ['1', '2', '3', '4', '5', '0']
    opcion = ''
    while opcion not in opciones_validas:
        print()
        print("[0m=========================") # [0m resetea colores      
        print("   GESTIÓN DE UN VUELO   ")
        print("=========================")
        print(" 1 - Imprimir datos vuelo")
        print(" 2 - Imprimir claves ")
        print(" 3 - Añadir <pasajeros> ")        
        print(" 4 - Imprimir un valor")
        print(" 5 - Borrar clave ")
        print(" 0 - SALIR ")
        print("-----------------------------")    
        opcion = input("Dame la opción: ")
        if (opcion not in opciones_validas):
            print("[31mERROR: por favor, vuelve a intentarlo.")
        else:
            print()    

    #Respondemos a la opción seleccionada    
    if opcion == '1':  #Imprimir datos del diccionario
        print("   DATOS DEL VUELO:")
        print('   ----------------')
        for k,v in vuelo.items(): # se recorre keys y values
            print('%9s: %8s' %(k,v))
    elif opcion == '2': #Imprimir las claves del diccionario
        print("CLAVES: ", end='')
        for clave in vuelo.keys():
            print (clave, end=", ")
    elif opcion == '3': #Añadir la clave 'pasajeros' con su valor
        nPasajeros = input('Indica el número de passajeros en el viaje: ')
        if nPasajeros.isdigit(): # otra manera de comprobar que es un entero
            vuelo['pasajeros'] = nPasajeros
        else:
            print(f'[31mERROR: {nPasajeros} no es un número entero.')
    elif opcion == '4': #Dada una clave, imprimir un valor
        claveUser = input('Indica la clave del valor a mostrar: ')
        error = True
        for clave in vuelo.keys():
            if clave.lower() == claveUser.lower(): #para evitar case sensitive
                print(f'valor de {claveUser.lower()}: {vuelo[claveUser.lower()]}')
                error=False
                break
        if error:     
            print(f'[31mERROR: {claveUser} no se encuentra dentro de'
                    +' la información del vuelo.')

    elif opcion == '5': #Borrar una clave con su valor
        claveUser = input('Indica la clave a borrar: ')
        error = True
        for clave in vuelo.keys():
            if clave.lower() == claveUser.lower(): #para evitar case sensitive
                print(f'la "clave: valor" a borrar es {claveUser.lower()}:'
                       +f' {vuelo[claveUser.lower()]}')
                vuelo.pop(claveUser.lower())
                error=False
                break # sale del bucle for y continua 
        if error:     
            print(f'[31mERROR: {claveUser} no se encuentra dentro de'
                    +' la información del vuelo, luego no se puede borrar.')
                
    else:
        acaba = True        
print("Hasta pronto")