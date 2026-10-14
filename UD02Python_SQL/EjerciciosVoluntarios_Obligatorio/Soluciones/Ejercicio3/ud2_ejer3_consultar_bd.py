######################################
# UNIDAD 2 - Ejercicio 3             #
# Consultar base de datos (SOLUCIÓN) #
######################################
import sqlite3

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
    '''Imprimir jugadores existentes en la base de datos
       
       Parámetros de entrada: cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("IMPRIMIR JUGADORES")
    cursor.execute("SELECT * FROM JUGADORES")
    
    jugadores = cursor.fetchall()
    for jug in jugadores:
        print("Nombre: {} - Vida: {}".format(jug[0], jug[1]))

def imprimir_herramientas_jugador(cursor):
    '''Imprimir las herramientas de un jugador
       
       Parámetros de entrada: cursor de la base de datos
       Parámetros de salida: no hay
    '''    
    print("HERRAMIENTAS JUGADOR")
    jugador = input("Dame el nombre del jugador: ")

    cursor.execute("SELECT * FROM LISTA_HERRAMIENTAS WHERE jugador = ?", (jugador,))
    herramientas = cursor.fetchall()
    if len(herramientas) > 0:
        print('Herramientas: ', end='')
        for herr in herramientas:
            print(herr[1], '- ', end='')
        print()
    else:
        print("El jugador <{}> no tiene herramientas asociadas.".format(jugador))

def consultar_jugador(cursor):
    '''Comprueba si existe un jugador en la tabla JUGADORES.
       
       Parámetros de entrada: cursor de la bd
       Parámetros de salida: no hay
    '''
    print("CONSULTAR JUGADOR")
    jugador = input("Dame el nombre del jugador: ")
    
    cursor.execute("SELECT * FROM JUGADORES WHERE nombre = ?", (jugador, ))    
    registro = cursor.fetchone()
    if (registro == None):
        print("El jugador <{}> no existe".format(jugador))
    else:
        print("Nombre: {} - Vida: {}".format(registro[0], registro[1]))
        

def consultar_herramienta_jugador(cursor):
    '''Comprueba si existe el par jugador-herramienta.
       
       Parámetros de entrada: cursor de la bd
       Parámetros de salida: no hay
    '''
    print("CONSULTAR HERRAMIENTA-JUGADOR")
    jugador = input("Dame el nombre del jugador: ")
    herramienta = input("Dame herramienta: ")
    
    sql = "SELECT * FROM LISTA_HERRAMIENTAS WHERE jugador = ? AND herramienta = ?"
    cursor.execute(sql, (jugador, herramienta))    
    registro = cursor.fetchone()
    if (registro == None):
        print("El jugador <{}> no tiene la herramienta <{}>".format(jugador, herramienta))
    else:
        print("El jugador <{}> sí tiene la herramienta <{}>".format(jugador, herramienta))




# PROGRAMA PRINCIPAL -------------------------------------------
conexion = sqlite3.connect('ejers_voluntarios_ejer3.db') #Creamos la conexión a la base de datos
cursor = conexion.cursor() #Creamos el cursor

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
conexion.close()