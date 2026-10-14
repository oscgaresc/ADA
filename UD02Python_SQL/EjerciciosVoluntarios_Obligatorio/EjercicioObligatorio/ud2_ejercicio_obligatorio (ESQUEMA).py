########################################
# UNIDAD 2 - Ejercicio obligatorio     #
# Credenciales de jugadores (ESQUEMA)  #
########################################
import sqlite3

# DEFINICIÓN DE FUNCIONES --------------------------------------
def valida_opcion():
    '''Función que muestra un menú y valida que la opción sea correcta'''    

    opc_correctas = ['1', '2', '3', '4', '5', '0']
    
    #Mostramos el menú y solicitamos la operación al usuario
    opcion = ''
    while opcion not in opc_correctas:
        print()
        print("==================================")            
        print("     CREDENCIALES JUGADORES       ")
        print("==================================")
        print(" 1 - Imprimir jugadores")
        print(" 2 - Validar credencial ")       
        print(" 3 - Cambiar credencial ")
        print(" 4 - Insertar nuevo jugador ")
        print(" 5 - Borrar jugador ")
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
    
    
def existe_credencial(cursor, usuario, contras):
    '''Comprueba si existe una credencial en la tabla CREDENCIALES.
       
       Parámetros de entrada: cursor de la bd, usuario y contraseña.
       Parámetros de salida: devuelve True si existe y False en otro caso
    '''
    pass

    
def validar_credencial(cursor):
    '''Comprueba si existe el par jugador-contrasenya.
       
       Parámetros de entrada: cursor de la bd
       Parámetros de salida: no hay
    '''
    print("VALIDAR CREDENCIAL")
    pass
    
    
def cambiar_credencial(conexion, cursor):
    '''Modifica la contraseña de un jugador
       
       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("CAMBIAR CREDENCIAL")     
    pass


def insertar_jugador(conexion, cursor):
    '''Inserta una nueva herramienta en la base de datos

       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("INSERTAR JUGADOR")
    pass
        
       
def borrar_jugador(conexion, cursor):
    '''Borra el jugador y sus credenciales de la base de datos
       
       Parámetros de entrada: conexión y cursor de la base de datos
       Parámetros de salida: no hay
    '''
    print("BORRAR JUGADOR")
    pass


# PROGRAMA PRINCIPAL -------------------------------------------
conexion = sqlite3.connect('bd/ejer_obligatorio.db') #Creamos la conexión a la base de datos
cursor = conexion.cursor() #Creamos el cursor

opcion = valida_opcion()
while opcion != '0':
    if opcion == '1': #Imprimir jugadores
        imprimir_jugadores(cursor)
    elif opcion == '2': #Validar credencial
        validar_credencial(cursor)            
    elif opcion == '3': #Cambiar credencial
        cambiar_credencial(conexion, cursor)
    elif opcion == '4': #Insertar nuevo jugador
        insertar_jugador(conexion, cursor)    
    elif opcion == '5': #Borrar jugador
        borrar_jugador(conexion, cursor)
    opcion = valida_opcion()
conexion.close()