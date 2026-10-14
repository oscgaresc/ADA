CREATE TABLE IF NOT EXISTS LISTA_HERRAMIENTAS (
    jugador TEXT,
    herramienta TEXT,
    PRIMARY KEY(jugador, herramienta),
    FOREIGN KEY(jugador) REFERENCES JUGADORES(nombre)
    FOREIGN KEY(herramienta) REFERENCES HERRAMIENTAS(herramienta)
);

# nos vamos a la carpeta EJERCICIO1 y tecleamos sqlite3
# .open ejers_voluntarios_ejer1.db
# .databases
# .read ud2_ejer1_crear_tabla.sql
# .tables
# .schema LISTA_HERRAMIENTAS
# .exit
