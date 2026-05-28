def revisar_letras(cadena):
    conjunto = "aeiouAEIOU"
    cantidad = 0
    for caracter in cadena:
        if caracter in conjunto:
            cantidad = cantidad + 1
    return cantidad

def ejecutar():
    mensaje = "Programacion en Python"
    resultado = revisar_letras(mensaje)
    print("Vocales encontradas:", resultado)

if __name__ == "__main__":
    ejecutar()
