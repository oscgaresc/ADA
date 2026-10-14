###################################
# UNIDAD 2 - Ejercicio 2          #
# Poblar una tabla (SOLUCIÓN)     #
###################################
import sqlite3

conexion = sqlite3.connect('ejers_voluntarios_ejer2.db') #Creamos la conexión a la base de datos
cursor = conexion.cursor() #Creamos el cursor

#Usamos execute() sin parámetros
cursor.execute("INSERT INTO LISTA_HERRAMIENTAS VALUES('ana', 'alas')")

#Usamos execute() sin parámetros
jugador = 'ana'
herramienta = 'botines'
cursor.execute("INSERT INTO LISTA_HERRAMIENTAS VALUES(?, ?)", (jugador, herramienta))

#Usamos executemany()
lista = [('ana', 'rastrillo'), 
         ('pep', 'alas'), 
         ('pep', 'varita'), 
         ('mary', 'varita'),
         ('mary', 'esencia'), 
         ('mary', 'martillo'), 
         ('quico', 'botines'),
         ('quico', 'rastrilo'), 
         ('sandy', 'varita')]
cursor.executemany("INSERT INTO LISTA_HERRAMIENTAS VALUES(?, ?)", lista)

#Hacemos permanentes los cambios
conexion.commit()
conexion.close()

# comprobación de que está bien
# abrimos un terminal en la carpeta de este ejecicio y tecleamos sqlite3
# .databases
# .open ejers_voluntarios_ejer2.db
# .databases
# .tables
# select * from LISTA_HERRAMIENTAS;
# .exit

