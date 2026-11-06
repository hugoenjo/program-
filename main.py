

def imprimir_tablero(tablero):
    print()
    print(f" {tablero[0]} | {tablero[1]} | {tablero[2]} ")
    print("---+---+---")
    print(f" {tablero[3]} | {tablero[4]} | {tablero[5]} ")
    print("---+---+---")
    print(f" {tablero[6]} | {tablero[7]} | {tablero[8]} ")
    print()


def casilla_libre(tablero, posicion):
    return tablero[posicion] == " "


def hay_ganador(tablero):
    combinaciones_ganadoras = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in combinaciones_ganadoras:
        if tablero[a] != " " and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]

    return None


def hay_empate(tablero):
    return " " not in tablero and hay_ganador(tablero) is None


def minimax(tablero, maximizando, profundidad=0):
    ganador = hay_ganador(tablero)

    if ganador == "O":
        return 10 - profundidad

    if ganador == "X":
        return profundidad - 10

    if hay_empate(tablero):
        return 0

    if maximizando:
        mejor_puntuacion = -float("inf")

        for posicion in range(9):
            if casilla_libre(tablero, posicion):
                tablero[posicion] = "O"

                puntuacion = minimax(
                    tablero, False, profundidad + 1
                )

                tablero[posicion] = " "

                mejor_puntuacion = max(
                    mejor_puntuacion, puntuacion
                )

        return mejor_puntuacion

    else:
        mejor_puntuacion = float("inf")

        for posicion in range(9):
            if casilla_libre(tablero, posicion):
                tablero[posicion] = "X"

                puntuacion = minimax(
                    tablero, True, profundidad + 1
                )

                tablero[posicion] = " "

                mejor_puntuacion = min(
                    mejor_puntuacion, puntuacion
                )

        return mejor_puntuacion


def mejor_movimiento(tablero):
    mejor_puntuacion = -float("inf")
    mejor_posicion = None

    for posicion in range(9):
        if casilla_libre(tablero, posicion):
            tablero[posicion] = "O"

            puntuacion = minimax(tablero, False, 1)

            tablero[posicion] = " "

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_posicion = posicion

    return mejor_posicion


def movimiento_maquina(tablero):
    posicion = mejor_movimiento(tablero)

    if posicion is not None:
        tablero[posicion] = "O"
        print("La máquina ha elegido la casilla:", posicion + 1)


def jugar():
    tablero = [" "] * 9
    jugador = "X"
    partida_terminada = False

    print("\nBIENVENIDO AL TRES EN RAYA")
    print("Juegas contra una inteligencia artificial.")
    print("Tú eres X y la máquina es O.")
    print("Las casillas se numeran del 1 al 9.")

    while not partida_terminada:
        imprimir_tablero(tablero)

        if jugador == "X":
            print("Tu turno.")

            try:
                posicion = int(input("Elige una casilla (1-9): "))

                if posicion < 1 or posicion > 9:
                    print("Elige una posición entre 1 y 9.")
                    continue

                posicion -= 1

                if not casilla_libre(tablero, posicion):
                    print("Esa casilla está ocupada.")
                    continue

            except ValueError:
                print("Introduce un número válido.")
                continue

            tablero[posicion] = "X"

        else:
            print("Turno de la máquina.")
            movimiento_maquina(tablero)

        ganador = hay_ganador(tablero)

        if ganador is not None:
            imprimir_tablero(tablero)

            if ganador == "X":
                print("¡Has ganado!")
            else:
                print("¡La máquina ha ganado!")

            partida_terminada = True

        elif hay_empate(tablero):
            imprimir_tablero(tablero)
            print("¡La partida ha terminado en empate!")
            partida_terminada = True

        else:
            jugador = "O" if jugador == "X" else "X"


def main():
    print("================================")
    print("          TRES EN RAYA")
    print("================================")

    jugar()


if __name__ == "__main__":
    main()
