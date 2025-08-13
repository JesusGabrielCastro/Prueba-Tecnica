#Escribe una función en lenguaje de su preferencia que tome una lista de
#enteros y un entero de destino, y devuelva los índices de los dos números
#que sumados dan el resultado del entero destino.


def encontrar_indices1(lista, objetivo):
    diccionario = {}
    for i, num in enumerate(lista):
        complemento = objetivo - num
        if complemento in diccionario:
            return (diccionario[complemento], i)
        diccionario[num] = i
    return None

def encontrar_indices2(lista, objetivo):
    combinaciones = []
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] + lista[j] == objetivo:
                combinaciones.append((i, j))
    return combinaciones if combinaciones else None

if __name__ == "__main__":
    numeros = [2, 7, 11, 15, 3, 6, 9, 4, 5, 8, 10, 12, 14, 13, 1]
    objetivo = 14
    resultado = encontrar_indices2(numeros, objetivo)
    if resultado:
        print(f"Los índices de los números que suman {objetivo} son: {resultado}")
    else:
        print(f"No se encontraron dos números que sumen {objetivo}.")


# salida esperada con la funcion encontrar_indices2:
# Los índices de los números que suman 14 son: [(0, 11), (2, 4), (5, 9), (6, 8), (7, 10), (13, 14)]

#salida esperada con la funcion encontrar_indices1:
# Los índices de los números que suman 14 son: (0, 11)
# esto ya que la función encontrar_indices1 devuelve solo el primer par de índices que encuentra.
# Si se desea obtener todos los pares no repetidos, se debe usar encontrar_indices2.