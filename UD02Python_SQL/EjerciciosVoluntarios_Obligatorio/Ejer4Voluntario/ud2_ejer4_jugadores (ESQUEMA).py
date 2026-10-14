###################################
# UNIDAD 2 - Ejercicio 4          #
# Jugadores (ESQUEMA)             #
###################################
import sqlite3

# DEFINICIÓN DE FUNCIONES --------------------------------------
def valida_opcion():
    '''Función que muestra un menú y valida que la opción sea correcta'''    

    opc_correctas = ['1', '2', '3', '4', '5', '0']
    
    #Mostramos el menú y solicitamos la operación al usuario
    opcion = ''
    while opcion not in opc_correctas:
        print()
        print("========================================")            
        print("         GESTIONANDO JUGADORES          ")
        print("========================================")
        print(" 1 - Imprimir jugadores")
        print(" 2 - Modificar vida de jugador ")
        print(" 3 - Insertar nuevo jugador ")
        print(" 4 - Imprimir herramientas-jugador ")
        print(" 5 - Quitar herramienta-jugador ")
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
    pass


def existe_jugador(cursor, jugador):
    '''Comprueba si existe un jugador en la tabla JUGADORES.
       
       Parámetros de entrada: cursor de la bd y nombre del jugador
       Parámetros de salida: devuelve True si existe y False en otro caso
    '''
    pass

    
def lee_vida():
    '''Pide el valor "vida" por pantalla.
       
       Parámetros de entrada: no hay
       Parámetros de salida: número entero vida
    '''    
    correcto = False
    while not correcto:
        try:
            vida = int(input("Dame vida: "))
        except ValueError:
            print("Estábamos esperando un número entero. Por favor, vuelve a intentarlo.")
        else:
            correcto = True
    return vida
        
def modificar_vida(conexion, cursor):
    '''Modifica la vida de un jugador
       
       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("MODIFICAR VIDA")
    pass

def insertar_jugador(conexion, cursor):
    '''Inserta una nueva herramienta en la base de datos

       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("INSERTAR JUGADOR")
    pass
        
        
def imprimir_herramientas_jugador(cursor):
    '''Imprimir las herramientas de un jugador
       
       Parámetros de entrada: cursor de la base de datos
       Parámetros de salida: no hay
    '''    
    print("HERRAMIENTAS JUGADOR")
    pass
        

def existe_herramienta_jugador(cursor, jugador, herramienta):
    '''Comprueba si existe el par jugador-herramienta.
       
       Parámetros de entrada: cursor de la bd, nombre del jugador y nombre de la herramienta
       Parámetros de salida: devuelve True si existe y False en otro caso
    '''
    pass


def quitar_herramienta(conexion, cursor):
    '''Borrar herramienta de la base de datos
       
       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("QUITAR HERRAMIENTA")
    pass

# PROGRAMA PRINCIPAL -------------------------------------------
conexion = ... #Creamos la conexión a la base de datos
cursor = ... #Creamos el cursor

opcion = valida_opcion()
while opcion != '0':
    if opcion == '1': #Imprimir jugadores
        imprimir_jugadores(cursor)
    elif opcion == '2': #Modificar vida de jugador
        modificar_vida(conexion, cursor)            
    elif opcion == '3': #Insertar nuevo jugador
        insertar_jugador(conexion, cursor)
    elif opcion == '4': #Imprimir herramientas-jugador
        imprimir_herramientas_jugador(cursor)
    elif opcion == '5': #Quitar herramienta-jugador
        quitar_herramienta(conexion, cursor)
    opcion = valida_opcion()
conexion.close()