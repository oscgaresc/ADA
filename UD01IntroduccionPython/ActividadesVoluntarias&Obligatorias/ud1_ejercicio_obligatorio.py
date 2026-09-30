############################################
# UNIDAD 1 - Ejercicio obligatorio         #
# Lista de vuelos                          #
############################################

vuelos = [{'origen':'Valencia', 'destino':'Menorca', 'día':'15-08', 'clase':'turista'},
          {'origen':'Valencia', 'destino':'Tenerife', 'día':'20-08', 'clase':'turista'},
          {'origen':'París', 'destino':'Valencia', 'día':'15-08', 'clase':'primera'},
          {'origen':'Atenas', 'destino':'Valencia', 'día':'20-08', 'clase':'primera'} ]

# DEFINICIÓN DE FUNCIONES --------------------------------------
def valida_opcion():
    '''Función que muestra un menú y valida que la opción sea correcta'''    
    
    #Mostramos el menú y solicitamos la operación al usuario
    opciones_validas = ['1', '2', '3', '4', '0'] # Elimino la opción 5 ya que no aparece
    opcion = ''
    while (opcion not in opciones_validas):
        print()
        print("[0m=========================") # Reseteando los colores        
        print("     LISTA DE VUELOS     ")
        print("=========================")
        print(" 1 - Imprimir datos vuelos")
        print(" 2 - Buscar por origen ")
        print(" 3 - Imprimir un vuelo")        
        print(" 4 - Cambiar fecha de vuelo ")        
        print(" 0 - SALIR ")
        print("-----------------------------")    
        opcion = input("Dame la opción: ")
        if (opcion not in opciones_validas):
            print("[31mError: por favor, vuelve a intentarlo.") # En rojo
        else:
            print()       
    return opcion

def imprimir(lista):
    '''Función que imprime la lista de vuelos.
    
       Parámetros de entrada: lista de diccionarios
       Parámetros de salida: no hay
    '''
    print("IMPRIMIR VUELOS:",end=' ')
    c = 0 # contador
    for vuelo in lista:
        c+=1
        print(f'\nvuelo {c} ', end='=> ')
        for k,v in vuelo.items():
            print('%8s: %8s' %(k,v), end= ',')

def buscar_origen(lista):
    '''Función que busca un vuelo dentro de una lista de vuelos.
    
       Parámetros de entrada: lista de diccionarios
       Parámetros de salida: no hay
    '''
    print("BUSCAR ORIGEN:",end=' ')
    c = 0 # contador
    origenVuelo = input('Indica el origen del vuelo a buscar: ')
    # doble búcle cíclico para obtener los datos de los objetos de la lista
    for vuelo in lista:     
        if vuelo['origen'].lower() == origenVuelo.lower().strip():
            c+=1
            print(f'\nvuelo {c} ', end='=> ')
            #imprimiendo los datos del vuelo
            for k,v in vuelo.items():
                    print('%8s: %8s' %(k,v), end= ',')
            #break # si solo queremos que encuentre el primero
    print() # espacio tras la lista
    if c == 0:
        print(f'[31mERROR: No hay vuelo con origen en: {origenVuelo}')

def imprimir_vuelo(lista):
    '''Función que imprime los datos de un vuelo.
    
       Parámetros de entrada: lista de diccionarios
       Parámetros de salida: no hay
    '''
    print("IMPRIMIR VUELO:")
    c = 0 # contador
    origen = input('Indica el origen del vuelo: ').lower().strip()
    destino = input('Indica el destino del vuelo: ').lower().strip()
    for vuelo in lista:
        if vuelo['origen'].lower() == origen and vuelo['destino'].lower() == destino:
            c+=1
            print(f'\n- Vuelo.')
            #imprimiendo los datos del vuelo
            for k,v in vuelo.items():
                print('%8s: %8s' %(k,v))
            #break # si solo queremos que encuentre el primero
    if c == 0:
        print(f'[31mERROR: No hay vuelo con origen "{origen}" y destino'
            +f' "{destino}". Revise su vuelo y verifique los datos, gracias.')

def cambiar_fecha(lista):
    '''Función que cambia la fecha de un vuelo.
    
       Parámetros de entrada: lista de diccionarios
       Parámetros de salida: lista de diccionarios actualizada
    '''
    print("CAMBIAR FECHA DE VUELO:")
    c = 0 # contador
    nuevaFecha = ''
    orig = input('Indica el origen del vuelo: ').lower().strip()
    dest = input('Indica el destino del vuelo: ').lower().strip()
    for vuelo in lista:
        if vuelo['origen'].lower() == orig and vuelo['destino'].lower() == dest:
            c+=1
            nuevaFecha = input(f"El vuelo de {orig} a {dest} saldrá el día {vuelo['día']}"
                               +f". Indique el cambio de fecha (dd-mm o ENTER"
                               +" para salir): ").strip()
            if nuevaFecha: # en caso de añadir enter, no modifica los datos
                #No hay protección en los datos del cambio de día
                vuelo['día'] = nuevaFecha
                print(f'\n- IMPRIMIENDO VUELO MODIFICADO.')
            else:
                print(f'\n- IMPRIMIENDO VUELO SIN CAMBIOS.')
            #imprimiendo los datos del vuelo    
            for k,v in vuelo.items():
                print('%8s: %8s' %(k,v))
            break # si solo queremos que encuentre el primero y lo modifique
    if c == 0:
        print(f'[31mERROR: No hay vuelo con origen "{orig}" y destino'
            +f' "{dest}". Revise su vuelo y verifique los datos, gracias.')     
    return lista # obligatorio si no queremos recibir un None

# PROGRAMA PRINCIPAL -------------------------------------------
opcion = valida_opcion()
while opcion != '0':          
    #Respondemos a la opción seleccionada    
    if opcion == '1':  
        imprimir(vuelos)
    elif opcion == '2': 
        buscar_origen(vuelos)
    elif opcion == '3': 
        imprimir_vuelo(vuelos)
    elif opcion == '4': 
        vuelos = cambiar_fecha(vuelos)
    opcion = valida_opcion()
    
print("Hasta pronto")
