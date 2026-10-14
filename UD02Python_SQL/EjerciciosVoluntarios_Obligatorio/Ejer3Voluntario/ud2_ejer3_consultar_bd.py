######################################
# UNIDAD 2 - Ejercicio 3             #
# Consultar base de datos (ESQUEMA)  #
######################################
import sqlite3
import os # también para evitar problemas rutas

# DEFINICIÓN DE FUNCIONES --------------------------------------
def valida_opcion():
    '''Función que muestra un menú y valida que la opción sea correcta'''    

    opc_correctas = ['1', '2', '3', '4', '0']
    
    #Mostramos el menú y solicitamos la operación al usuario
    opcion = ''
    while opcion not in opc_correctas:
        print()
        print("========================================")            
        print("         CONSULTAR BASE DE DATOS        ")
        print("========================================")
        print(" 1 - Imprimir jugadores")
        print(" 2 - Imprimir herramientas-jugador ")
        print(" 3 - Consultar jugador")
        print(" 4 - Consultar herramienta-jugador")
        print(" 0 - SALIR ")
        print("--------------------------")    
        opcion = input("Dame la opción: ")
        if opcion not in opc_correctas:
            print("Por favor, vuelve a intentarlo.")
        else:
            print()       
    return opcion
    
def imprimir_jugadores(cursor):
    '''Imprimir jugadores existentes en la base de datos.

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.
       
    Returns:
       Out: No hay. Muestra por consola las columnas nombre y vida de la tabla JUGADORES de la BDA.
    '''
    print("IMPRIMIR JUGADORES")
    cursor.execute('SELECT nombre, vida from JUGADORES')
    # fechone() / fetchall() para recuperar los resultados
    reg = cursor.fetchone() # retorna la tupla con los valores de las columnas 
    c = 0 # contador de jugadores
    while reg != None: # None si no hay nada que retornar
        c+=1
        print(f'jugador {c:>2}: Nombre: {reg[0]:<6} - Vidas: {reg[1]:>3} ')
        reg = cursor.fetchone() # siguiente registro

def imprimir_herramientas_jugador(cursor):
    '''Imprimir las herramientas de un jugador

    Args
    ---
     cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        No hay. Muestra por consola las herramientas de un jugador seleccionado por el usuario.
    '''    
    print("HERRAMIENTAS JUGADOR")
    cursor.execute('SELECT * from LISTA_HERRAMIENTAS')
        # fechone() / fetchall() para recuperar los resultados
    registros = cursor.fetchall() # retorna tupla con los valores de todas las columnas 
    nombre = input ('Para conocer las herramientas de un jugador, indica su nombre: ')
    estaRegistrado = False # centinela 
    herramientas = [] # lista de herramientas vacía
    for reg in registros:
        if reg[0]==nombre.lower(): # Compara la columna 0, es decir, la columna nombre de la tabla
            herramientas.append(reg[1]) # se añade la herramienta de la columna 1 a la lista
            estaRegistrado = True
    if not estaRegistrado:
        print(f'\u001B[33mWARNING: El jugador {nombre} no se encuentra'
              +f' en la base de datos.\u001B[0m')
    else:
        print(f'El/la jugador/a {nombre} tiene las herramientas:', end=" ")
        for elem in herramientas:
              print(f'{elem}', end=' - ')
    print()
            
def consultar_jugador(cursor):
    '''Comprueba si existe un jugador en la tabla JUGADORES.
    Args
    ---
     cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        No hay. Muestra por consola las vidas de un jugador seleccionado por el usuario.
    '''
    print("CONSULTAR JUGADOR")
    cursor.execute('SELECT * from JUGADORES')
            # fechone() / fetchall() para recuperar los resultados
    registros = cursor.fetchall() # retorna tupla con los valores de las columnas 
    nombre = input ('Para conocer las vidas de un jugador, indica su nombre: ')
    estaRegistrado = False # centinela
    vida = ''
    for reg in registros:
        if reg[0]==nombre.lower():
            vida = reg[1]
            estaRegistrado = True
    if not estaRegistrado:
        print(f'\u001B[33mWarning: El jugador {nombre} no se encuentra'
              +f' en la base de datos.\u001B[0m')
    else:
        print(f'El/la jugador/a {nombre} tiene una vida de: {vida}')

def consultar_herramienta_jugador(cursor):
    '''Comprueba si existe el par jugador-herramienta.

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        No hay. Muestra por consola la relación entre un jugador seleccionado por el usuario y sus herramientas.
    '''
    print("CONSULTAR HERRAMIENTA-JUGADOR")
    cursor.execute('SELECT * from LISTA_HERRAMIENTAS')
    # fechone() / fetchall() para recuperar los resultados
    registros = cursor.fetchall() # retorna tupla con los valores de las columnas 
    nombre = input ('Indica el nombre del jugador: ')
    estaRegistrado = False # centinela
    herramientas = [] # lista de herramientas vacía
    for reg in registros:
        if reg[0]==nombre.lower():
            herramientas.append(reg[1])
            estaRegistrado = True    
    if len(herramientas) == 0 or not estaRegistrado: 
        print(f'\u001B[33mWarning: El jugador {nombre} no se encuentra'
                      +f' en la base de datos o no tiene herramientas.\u001B[0m')
    else:
        eina = input ('Indica el nombre de la herramienta: ')
        for h in herramientas:
            #ternaria
            if h == eina:
                estaRegistrado = True
                break
            else: estaRegistrado = False

        if estaRegistrado:
            print(f'El/la jugador/a {nombre} tiene la herramienta: {eina}')
        else:
            print(f'\u001B[33mWarning: El/la jugador/a {nombre} No tiene'
                  +f' la herramienta: {eina}\u001B[0m')

# PROGRAMA PRINCIPAL -------------------------------------------
#se muestra la ruta de trabajo actual amb el metode getcwd() ""
print(f"Trabajando en la ruta:\n{os.getcwd()}")
ruta_fichero = input("\nIndica la ruta relativa hasta el fichero .db"
                     +" (intro si es la misma): ") 
# EjerciciosVoluntarios_Obligatorio\Ejer3Voluntario
nomFichero = input('\nIndica el nombre del fichero de la BD: ')
# ejers_voluntarios_ejer3.db
ruta_completa = os.path.join(os.getcwd(), ruta_fichero, nomFichero) #directorio real de trabajo 
print (f'Ruta a conectar: {ruta_completa}')
conexion = sqlite3.connect(ruta_completa)
#Se abre la conexión con la base de datos
cursor = conexion.cursor()

opcion = valida_opcion()
while opcion != '0':
    if opcion == '1': #Imprimir jugadores
        imprimir_jugadores(cursor)
    elif opcion == '2': #Imprimir herramientas-jugadores
        imprimir_herramientas_jugador(cursor)
    elif opcion == '3': #Consultar jugador
        consultar_jugador(cursor)
    elif opcion == '4': #Consultar herramienta-jugador
        consultar_herramienta_jugador(cursor)
        
    opcion = valida_opcion()
#Se cierra la conexión con la base de datos.
conexion.close()