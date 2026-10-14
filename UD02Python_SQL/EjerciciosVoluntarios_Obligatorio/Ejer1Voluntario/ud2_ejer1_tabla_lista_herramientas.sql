######################################
# UNIDAD 2 - Ejercicio 1             #
# crear la tabla LISTA_HERRAMIENTAS  #
######################################
# sqlite3
# .open ejers_voluntarios_ejer1.db
# .read ud2_ejer1_tabla_lista_herramientas.sql

.mode column
# las tablas JUGADORES y HERRAMIENTAS ya están creadas
# CREATE TABLE IF NOT EXISTS JUGADORES (
#   nombre TEXT,
#    PRIMARY KEY(nombre)
# );

# CREATE TABLE IF NOT EXISTS HERRMIENTAS(
#    nombre TEXT,
#    PRIMARY KEY(nombre)
# );

CREATE TABLE IF NOT EXISTS LISTA_HERRAMIENTAS (
    jugador TEXT,
    herramienta TEXT,
    PRIMARY KEY(jugador, herramienta),
    FOREIGN KEY(jugador) REFERENCES JUGADORES(nombre),
    FOREIGN KEY(herramienta) REFERENCES HERRAMIENTAS(nombre)
);