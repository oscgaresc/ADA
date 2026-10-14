######################################
# UNIDAD 2 - Ejercicio 1             #
# poblar la tabla LISTA_HERRAMIENTAS #
######################################

# importar libreria del SGBD sqlite
import sqlite3
import os # también para evitar problemas rutas

#se muestra la ruta de trabajo actual amb el metode getcwd() ""
print(f"Trabajando en la ruta:\n{os.getcwd()}")


ruta_fichero = input("\nIndica la ruta relativa hasta el fichero .db"
                     +" (intro si es la misma): ") 
# EjerciciosVoluntarios_Obligatorio\Ejer2Voluntario
nomFichero = input('\nIndica el nombre del fichero: ')
# ejers_voluntarios_ejer2.db
ruta_completa = os.path.join(os.getcwd(), ruta_fichero, nomFichero) #directorio real de trabajo 
# print(f'Ruta de trabajo actual: {ruta_completa}')

# conectando a la base de datos ejers_voluntarios_ejer2.db
my_conn = sqlite3.connect(ruta_completa)

# generando el cursos u objeto de la BD para ejecutar instrucciones SQL
my_cur = my_conn.cursor()
# sentencias/instrucciones 
# insert directo
ins1 = '''insert into LISTA_HERRAMIENTAS
    values ('ana', 'alas')'''
# cuidado con las "" en los TEXT, se interpretan como atributo de la
# tabla no como dato
    
# insert con dos parámetros ??
ins2 = ''' INSERT INTO LISTA_HERRAMIENTAS
    VALUES(?, ?)''' # con dos parámetros y una tupla 
# # insert con una lista de tuplas
lista = [('ana', 'rastrillo'),
         ('pep', 'alas'),
         ('pep', 'varita'),
         ('mary', 'varita'),
         ('mary', 'esencia'),
         ('mary', 'martillo'),
         ('quico', 'botines'),
         ('quico', 'rastrilo'),
         ('sandy', 'varita')]
 
# utilizando execute()
#sin parámetros
my_cur.execute(ins1) #insertando una linea de datos
# con dos parámetros
my_cur.execute(ins2,('ana','botines')) # hay que añadir los parámetros en una tupla
# # con una lista de tuplas
my_cur.executemany(ins2,lista) 


my_conn.commit() # un commit por transacción

# cerrando la conexión a la BD
my_conn.close()

print("\n¡Tabla verificada e inserciones realizadas con éxito!")