###################################
# UNIDAD 1 - Ejercicio 3          #
# Jugadores on-line (ESQUEMA)     #
###################################

# Creando una función para imprimir listas
def imprimiendoLista(lista):
    #Imprimimos la lista de jugadores on-line
    print('\nlista de jugadores on-line'.upper())
    c = 1 # contador
    for elemento in lista:
        print(f'Jugador {c}: {elemento}', end=' - ')
        c+=1

#Creamos la lista con todos los jugadores on-line que hay conectados
jugadores = ["mario", "mafalda", "luigi", "esther", "heidi", "songoku", "beauty", "beast"]

imprimiendoLista(jugadores)

acaba = False
while not acaba:      
    #mostramos el menú y solicitamos la operación al usuario
    print('\n\n[0m==================================') # resetea colores
    print('\tJUGADORES ON-LINE')
    print('==================================')
    print('1 - Llega un jugador nuevo')
    print('2 - Se va un jugador')
    print('3 - Fin')
    # bucle try-exception para controlar el mensaje de error cuando
    # el usuario no añada un entero
    try:
        opcion = int(input('Indica la opción seleccionada (1-3): '))

        #Respondemos a la opción seleccionada    
        if opcion == 1:
            #preguntamos el nombre, damos la bienvenida y añadimos a la lista
            nom = input('¿Cómo te llamas? ')
            print(f'Bienvenido@ jugador {nom}')
            jugadores.append(nom)
            #Imprimiendo lista
            imprimiendoLista(jugadores)

        elif opcion == 2:
            print(f'Adiós al jugador {jugadores[0]}')
            jugadores.pop(0) # borrando el 1º elemento de la lista
            #Imprimiendo lista
            imprimiendoLista(jugadores)

        elif opcion == 3:
            acaba = True  
        else:
             print(f'[31mERROR: {opcion} no es un nº entero entre 1 y 3, vuelve a intentarlo.')
                    
    except ValueError:
        print("[31mError. El dato no es un entero, vuelve a intentarlo.")
    
print("Hasta pronto") # resetea los colores
print()