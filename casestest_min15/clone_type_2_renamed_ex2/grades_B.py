def asignar_letras(calificaciones):
    salida = []
    for nota in calificaciones:
        if nota >= 90:
            letra = "A"
        elif nota >= 80:
            letra = "B"
        elif nota >= 70:
            letra = "C"
        else:
            letra = "F"
        salida.append(letra)
    return salida

def principal():
    calificaciones = [71, 99, 64, 85, 100]
    letras = asignar_letras(calificaciones)
    for nota, letra in zip(calificaciones, letras):
        print(nota, "->", letra)

principal()
