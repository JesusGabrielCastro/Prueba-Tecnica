#Escribe una función en lenguaje de su preferencia que tome una lista de
#enteros y un entero de destino, y devuelva los índices de los dos números
#que sumados dan el resultado del entero destino.


def encontrar_indices1(numeros, suma_buscada):
    valores_vistos = {}
    for posicion, numero_actual in enumerate(numeros):
        numero_faltante = suma_buscada - numero_actual
        if numero_faltante in valores_vistos:
            return (valores_vistos[numero_faltante], posicion)
        valores_vistos[numero_actual] = posicion
    return None



if __name__ == "__main__":
    numeros = [2, 7, 11, 15, 3, 6, 9, 4, 5, 8, 10, 12, 14, 13, 1]
    objetivo = 14
    resultado = encontrar_indices1(numeros, objetivo)
    if resultado:
        print(f"Los índices de los números que suman {objetivo} son: {resultado}")
    else:
        print(f"No se encontraron dos números que sumen {objetivo}.")



#salida esperada con la funcion encontrar_indices1:
# Los índices de los números que suman 14 son: (0, 11)
# esto ya que la función encontrar_indices1 devuelve solo el primer par de índices que encuentra.