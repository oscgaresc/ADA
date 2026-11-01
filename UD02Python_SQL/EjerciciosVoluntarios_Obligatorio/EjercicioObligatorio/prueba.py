

# nums = [1,2,4,6,8]
# print("[", end="")
# for i in pipe_fix(nums):
#     print(i, end=", ")

# print("]")
def mi_alternativo(string):
    lista_temp = []
    lista = list(string) # sin nada
    for c in lista:
        # Transformamos y guardamos en la lista (muy rápido)
        if c.isupper():
            lista_temp.append(c.lower()) 
        else:
            lista_temp.append(c.upper())
        # Unimos todo de golpe al final
    return "".join(lista_temp)

resultado = mi_alternativo("Hola ComO EStAS?")
print(resultado)