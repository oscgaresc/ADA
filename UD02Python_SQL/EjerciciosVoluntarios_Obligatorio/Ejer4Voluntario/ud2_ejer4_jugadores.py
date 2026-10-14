###################################
# UNIDAD 2 - Ejercicio 4          #
# Jugadores (ESQUEMA)             #
###################################
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

def existe_herramienta_jugador(cursor, jugador, herramienta):
    '''Comprueba si existe el par jugador-herramienta.

    Args
    ---
    cursor (cursor)   
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.
    jugador (string)
        necesario para comparar con los jugadores de la BDA.
    herramientas (string)
            necesario para comparar con las herramientas de la BDA.

    Returns:
        Boolean: devuelve True si existe y False en otro caso.
    ''' 
    #Buscando en la BDA el registro indicado por el usuario
    cursor.execute('SELECT * from LISTA_HERRAMIENTAS where jugador = ? AND '+
                   'herramienta = ?',(jugador,herramienta))
    # fechone() / fetchall() para recuperar el resultado específico
    registros = cursor.fetchone() # retorna tupla con el único valor seleccionado
    # cuidado con fetchall() aquí 
    return (registros != None)
    
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
            vida = int(input("Dame vida: ").strip())
        except ValueError:
            print("\u001B[33mWARNING: Se está esperando un número entero. Por favor,"
                +" vuelve a intentarlo.\u001B[0m")
        else:
            correcto = True
    return vida
        
def modificar_vida(conexion, cursor):
    '''Modifica la vida de un jugador

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())
        Para realizar realizar un commit al update que se realiza en la BDA.

    Returns:
        No hay. Se muestra por consola que se ha actualizado la "vida" en la BDA.
    '''
    print("MODIFICAR VIDA")
    nombre = input ('Indica el nombre del jugador: ').lower().strip()
    if not existe_jugador(cursor, nombre):
        print(f'\u001B[33mWARNING: El/la jugador/a {nombre} no existe.\u001B[0m')
        return
    vida = lee_vida() # Solicita vida al usuario
    
    cursor.execute('update JUGADORES set vida = ? where nombre = ?'
                   ,(int(vida),nombre)) # siempre con tupla
    conexion.commit()
    print(f'\u001B[32mSe ha actualizado la vida al jugador/a {nombre}.\u001B[0m')

    # Se puede realizar directamente en update a través de los datos del usuario
    # y utilizar cursor.rowcount donde el caso de devolver un 0 quiere decir que
    # no se ha actualizado ningún jugador de la tabla JUGADORES, por tanto, el
    # nombre del jugador no existe en la base de datos.

def insertar_jugador(conexion, cursor):
    '''Inserta una nuevo jugador en la base de datos

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())
        Para realizar realizar un commit al insert que se realiza en la BDA.

    Returns:
        No hay. Se muestra por consola que se ha añadido un jugador en la BDA.
    '''
    print("INSERTAR JUGADOR")
    nombre = input ('Indica el nombre del jugador: ').lower().strip()
    if existe_jugador(cursor, nombre):
        print(f'\u001B[33mWARNING: el/la jugador/a {nombre} ya existe.\u001B[0m')
        return
    vida = lee_vida() # Solicita vida del jugador al usuario.
    ins = 'insert into JUGADORES values(?,?)'
    cursor.execute(ins,(nombre, int(vida))) # int para asegurar el entero
    conexion.commit()
    print(f'\u001B[32mSe ha insertado el jugador/a "{nombre}" con vida {vida}.\u001B[0m')

def existe_herramienta_asociada_jugador(cursor, jugador):
    '''Comprueba si existe el una herramienta asociada al jugador en la tabla LISTA_HERRAMIENTAS

    Args
    ---
    cursor (cursor)   
        Objeto de la BDA que permite ejecutar instrucciones SQL y recuperar registros de la BDA.
    jugador (string)
        necesario para comparar con los jugadores de la BDA.

    Returns:
        Boolean: devuelve True si existe y False en otro caso.
    ''' 
        #Buscando en la BDA el registro indicado por el usuario
    cursor.execute('SELECT * from LISTA_HERRAMIENTAS where jugador = ?',(jugador,))
    # fechone() / fetchall() para recuperar los resultados
    registro = cursor.fetchall() # retorna tupla con los valores de las columnas
    # con los parámetros cursor y comprobado el nombre. 
    return len(registro)!= 0
        
        
def imprimir_herramientas_jugador(cursor):
    '''Imprimir las herramientas de un jugador

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.

    Returns:
        No hay. Se muestra por consola las herramientas de un jugador introducido.
    '''    
    print("HERRAMIENTAS JUGADOR")
    nombre = input ('Indica el nombre del jugador: ').lower().strip()
    if not existe_jugador(cursor, nombre.lower()):
        print(f'\u001B[33mWARNING: el/la jugador/a {nombre} no existe.\u001B[0m')
        return
    
    if not existe_herramienta_asociada_jugador(cursor, nombre):
        print(f'\u001B[33mWARNING: el/la jugador/a {nombre} no tiene asociada'+
              ' niguna herramienta.\u001B[0m')
        return
    cursor.execute('SELECT * from LISTA_HERRAMIENTAS where jugador = ?',(nombre,))
    # fechone() / fetchall() para recuperar los resultados
    registro = cursor.fetchall() # retorna tupla con los valores de las columnas
    
    print(f'El/la jugador/a {nombre} tiene las herramientas:', end=" ")
    for reg in registro:
        # se extrae los datos por su indice para evitar la tupla entera
        if reg[0]==nombre: # para buscar las herramientas del jugador introducido
            # se extrae los datos por su indice para evitar la tupla entera
            print(f'{reg[1]}', end=' - ') 

             
def quitar_herramienta(conexion, cursor):
    '''Borrar herramienta de la base de datos

    Args
    ---
    cursor (cursor)
        Objeto de la BDA que permite ejercutar instrucciones SQL y recuperar registros de la BDA.
    Conexion (sqlite3.connect())

    Returns:
        No hay. Elimina de la BDA la herramienta de un jugador seleccionado por el usuario.
    '''
    print("QUITAR HERRAMIENTA")
    nombre = input ('Indica el nombre del jugador: ').lower().strip()
    # Comprobando si el jugador se encuentra en la tabla JUGADORES
    if not existe_jugador(cursor, nombre):
            print(f'\u001B[33mWarning: el/la jugador/a {nombre} no existe.\u001B[0m')
            return # sale de la función
    # Comprobar si el jugador tiene asociada una herramienta
    if not existe_herramienta_asociada_jugador(cursor, nombre):
            print(f'\u001B[33mWARNING: el/la jugador/a {nombre} no tiene asociada'+
                  ' niguna herramienta.\u001B[0m')
            return
    herramienta = input ('Indica la herramienta del jugador: ').lower().strip()
    # con los parámetros cursor y comprobado el nombre, solo falta un bucle
    # condicional para borrar la herramienta indicada por el usuario.
    delHerramienta = '''delete from LISTA_HERRAMIENTAS
                where jugador = ? and herramienta = ?'''
    if existe_herramienta_jugador(cursor, nombre, herramienta ):
        cursor.execute(delHerramienta, (nombre, herramienta))
        conexion.commit()
        print(f'\u001B[32mSe ha eliminado correctamente la herramienta {herramienta}'
              +f' del jugador {nombre}\u001B[0m')
    else:
        print(f'\u001B[33mWarning: El/la jugador/a {nombre} No tiene'
                          +f' la herramienta: {herramienta}\u001B[0m')
        

# PROGRAMA PRINCIPAL -------------------------------------------
#se muestra la ruta de trabajo actual amb el metode getcwd() ""
print(f"Trabajando en la ruta:\n{os.getcwd()}")

ruta_fichero = input("\nIndica la ruta relativa hasta el fichero .db"
                     +" (intro si es la misma): ") 
# EjerciciosVoluntarios_Obligatorio\Ejer4Voluntario
nomFichero = input('\nIndica el nombre del fichero de la BD: ')
# ejers_voluntarios_ejer4.db
ruta_completa = os.path.join(os.getcwd(), ruta_fichero, nomFichero) #directorio real de trabajo 
#Se abre la conexión con la base de datos
conexion = sqlite3.connect(ruta_completa)
cursor = conexion.cursor()

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
#Se cierra la conexión con la base de datos.
conexion.close()