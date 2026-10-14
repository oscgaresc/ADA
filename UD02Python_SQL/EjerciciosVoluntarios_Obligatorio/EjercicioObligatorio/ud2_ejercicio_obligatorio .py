########################################
# UNIDAD 2 - Ejercicio obligatorio     #
# Credenciales de jugadores (ESQUEMA)  #
########################################
import pwinput
import os
import sqlite3

# DEFINICIÓN DE FUNCIONES --------------------------------------
def valida_opcion():
    '''Función que muestra un menú y valida que la opción sea correcta'''    

    opc_correctas = ['1', '2', '3', '4', '5', '0']
    
    #Mostramos el menú y solicitamos la operación al usuario
    opcion = ''
    while opcion not in opc_correctas:
        print()
        print("\u001B[0m==================================")            
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
            print("\u001B[33mWARNING:Por favor, vuelve a intentarlo.\u001B[0m")
        else:
            print()       
    return opcion
    
    
def imprimir_jugadores(cursor):
    '''Imprimir jugadores existentes en la base de datos

    Args
    ---
    cursor (cursor)   
        Objeto que permite ejecutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        Out: No hay. Muestra por consola las columnas nombre y vida de la tabla JUGADORES.
    '''
    print("IMPRIMIR JUGADORES")
    cursor.execute('SELECT nombre, vida from JUGADORES')
    # fechone() / fetchall() para recuperar los resultados
    reg = cursor.fetchone() # retorna tupla con los valores de las columnas 
    c = 0 # contador
    while reg != None: # None si no hay nada que retornar
        c+=1
        print(f'jugador {c:>2}: Nombre: {reg[0]:<6} - Vidas: {reg[1]:>3}')
        reg = cursor.fetchone() # siguiente registro   

def existe_jugador(cursor, jugador):
    '''Comprueba si existe un jugador en la tabla JUGADORES.

    Args
    ---
    cursor (cursor)   
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.
    jugador (string)
        necesario para comparar con los jugadores de la BDA.

    Returns:
        Boolean: devuelve True si existe y False en otro caso.
    ''' 
    cursor.execute('SELECT * from JUGADORES where nombre = ?',(jugador,))
    # fechone() / fetchall() para recuperar los resultados
    registro = cursor.fetchone() # retorna tupla con los valores de las columnas 
    return (registro != None) 
    
def existe_credencial(cursor, usuario, contras):
    '''Comprueba si existe una credencial en la tabla CREDENCIALES.

    Args
    ---
    cursor (cursor)   
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.
    usuario (string)
        necesario para poder tener acceso..
    contras (string)
            necesario para que el usuario tenga acceso.
       
    Returns:
        Boolean: devuelve True si existe y False en otro caso.
    '''
    cursor.execute('SELECT * from CREDENCIALES where usuario = ? '
                   +'and contrasenya = ?',(usuario,contras))
    # fechone() / fetchall() para recuperar los resultados
    registro = cursor.fetchone() # retorna tupla del valor de las columnas     
    return (registro != None)

def lee_vida():
    '''Pide el valor "vida" por pantalla.

    Args
    ---
        No hay.

    Returns:
        Integer: número de vida del jugador.
    '''    
    correcto = False
    while not correcto:
        try:
            vida = int(input("Dame vida: "))
        except ValueError:
            print("\n\u001B[33mWARNING:Se está esperando un número entero. "
                +"Por favor, vuelve a intentarlo.\n\u001B[0m")
        else:
            correcto = True
    return vida
    
def validar_credencial(cursor):
    '''Comprueba si existe el par jugador-contrasenya.

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        Out: No hay. Muestra por consola si la credencial es valida o no.
    '''
    print("VALIDAR CREDENCIAL")
    nombre = input ('Indica el nombre del jugador: ').lower().strip()
    # Confirmando usuario
    if not existe_jugador(cursor, nombre):
            print(f'\u001B[33mWARNING: El/la jugador/a {nombre} no existe.\u001B[0m')
            return # Sale de la función sin devolver nada

    # Se utiliza la libreria pwinput para ocultar las contrasenyas
    password = pwinput.pwinput('Ahora la contraseña del jugador: ',
                                mask='*')

    # Comprobando el par jugador-credenciales y evitar código duplicado
    print()
    if  existe_credencial(cursor, nombre, password):
        print(f'\u001B[32mLa contraseña introducida es correcta.\u001B[0m')
    else:
        print(f'\u001B[33mWARNING: La contraseña introducida '+
              f'NO es existe.\u001B[0m')    
    
def cambiar_credencial(conexion, cursor):
    '''Modifica la contraseña de un jugador.

    Args
    ---
    cursor (cursor)
        Permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())

    Returns:
        No hay. Actualiza la columna contrasenya de la tabla credenciales de la BDA.
    '''
    print("CAMBIAR CREDENCIAL")     
    nombre = input('Indica el nombre del jugador: ').lower().strip()

    if not existe_jugador(cursor, nombre):
        print(f'\n\u001B[33mWARNING: El/la jugador/a {nombre} no existe.\u001B[0m')
        return # Sale de la función sin devolver nada
    
    pwdOld = pwinput.pwinput('Ahora indica la contraseña a cambiar: ',
                             mask='*')
    if not existe_credencial(cursor, nombre, pwdOld):
        print(f'\n\u001B[33mWARNING: El contraseña introducida no es'
              +f' válida.\u001B[0m')
        return # Sale de la función sin devolver nada
    
    # Si supera las dos estructuras condicionales se modifica
    pwdNew = pwinput.pwinput('Por último, indica la nueva contraseña: ',
                             mask='*')
    mod = 'update CREDENCIALES set contrasenya = ? where usuario = ?'
    cursor.execute(mod,(pwdNew, nombre))
    conexion.commit()
    print(f'\n\u001B[32mLa contraseña del jugador "{nombre}" se ha'
          +' modificado correctamente.\u001B[0m')

def insertar_jugador(conexion, cursor):
    '''Inserta una nueva herramienta en la base de datos.

    Args
    ---
    cursor (cursor)
        Permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())

    Returns:
        No hay. Inserta un usuario, su vida y la contrasenya en la BDA.

    '''
    print("INSERTAR JUGADOR")
    nombre = input('Indica el nombre del jugador: ').lower().strip()

    if existe_jugador(cursor, nombre):
        print(f'\n\u001B[33mWARNING: El/la jugador/a {nombre} ya existe.\u001B[0m')
        return # Sale de la función sin devolver nada
    
    vida = lee_vida()

    pwd = pwinput.pwinput('\nPor último, la contraseña del nuevo jugador: ',
                          mask='*')
    # insertando los datos
    ins1 = 'insert into JUGADORES(nombre, vida) values(?, ?)'
    ins2 = 'insert into CREDENCIALES(usuario, contrasenya) values(?, ?)'
    cursor.execute(ins1,(nombre, vida))
    cursor.execute(ins2, (nombre, pwd))
    conexion.commit()
    print(f'\n\u001B[32mEl nuevo jugador "{nombre}" se ha insertado '+
          f'correctamente.\u001B[0m')        
       
def borrar_jugador(conexion, cursor):
    '''Borra el jugador y sus credenciales de la base de datos

    Args
    ---
    cursor (cursor)
        Permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())

    Returns:
        No hay. Elimina un usuario introducido de la BDA.

    '''
    print("BORRAR JUGADOR")
    nombre = input('Indica el nombre del jugador: ').lower()
    if not existe_jugador(cursor, nombre):
        print(f'\n\u001B[33mWARNING: El/la jugador/a {nombre} NO existe.\u001B[0m')
        return # Sale de la función sin devolver nada
    del1 = 'delete from JUGADORES where nombre = ?'
    del2 = 'delete from CREDENCIALES where usuario = ?'
    cursor.execute(del1, (nombre,))
    cursor.execute(del2, (nombre,))
    conexion.commit()
    print(f'\n\u001B[32mEl jugador "{nombre}" se ha borrado correctamente.\u001B[0m') 

# PROGRAMA PRINCIPAL -------------------------------------------
#Se crea la conexión a la base de datos
# --------------------------------------------------------------
#se muestra la ruta de trabajo actual amb el metode getcwd() ""
print(f"Trabajando en la ruta:\n{os.getcwd()}")

ruta_fichero = input("\nIndica la ruta relativa hasta el fichero .db"
                     +" (intro si es la misma): ") 
# EjerciciosVoluntarios_Obligatorio\EjercicioObligatorio
nomFichero = input('\nIndica el nombre del fichero de la BD: ')
# ejer_obligatorio.db
ruta_completa = os.path.join(os.getcwd(), ruta_fichero, nomFichero) #directorio real de trabajo 
#Se abre la conexión con la base de datos
conexion = sqlite3.connect(ruta_completa)
# ---------------------------------------------------------------
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
#Se cierra la conexión con la base de datos.
conexion.close()