"""Tres en raya contra una IA con Minimax, poda alfa-beta y mejoras.

La IA:
- Prioriza victorias y bloqueos inmediatos.
- Ordena los movimientos para facilitar la poda.
- Usa una tabla de transposiciones para reutilizar cálculos.
- Reconoce tableros simétricos (giros y reflejos).
- Prefiere ganar antes y perder más tarde.

Ejecuta: python main.py
"""

from math import inf


COMBINACIONES_GANADORAS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

CENTRO = (4,)
ESQUINAS = (0, 2, 6, 8)
LATERALES = (1, 3, 5, 7)


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
    for a, b, c in COMBINACIONES_GANADORAS:
        if tablero[a] != " " and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]
    return None


def hay_empate(tablero):
    return " " not in tablero and hay_ganador(tablero) is None


def transformaciones_simetricas(tablero):
    """Genera los ocho giros/reflejos del tablero como tuplas."""
    matriz = [list(tablero[i:i + 3]) for i in range(0, 9, 3)]
    reflejada = [fila[::-1] for fila in matriz]
    variantes = []

    for base in (matriz, reflejada):
        actual = base
        for _ in range(4):
            variantes.append(tuple(actual[fila][columna]
                                   for fila in range(3)
                                   for columna in range(3)))
            actual = [list(fila) for fila in zip(*actual[::-1])]

    return variantes


def clave_tablero(tablero, maximizando, profundidad):
    """Una misma posición girada o reflejada comparte clave de memoria."""
    simetria_canonica = min(transformaciones_simetricas(tablero))
    return simetria_canonica, maximizando, profundidad


def ordenar_movimientos(tablero, jugador):
    """Ordena primero las victorias, después bloqueos y casillas estratégicas."""
    rival = "X" if jugador == "O" else "O"
    movimientos = []

    for posicion in range(9):
        if not casilla_libre(tablero, posicion):
            continue

        tablero[posicion] = jugador
        victoria = hay_ganador(tablero) == jugador
        tablero[posicion] = " "

        if victoria:
            prioridad = 0
        else:
            tablero[posicion] = rival
            amenaza_rival = hay_ganador(tablero) == rival
            tablero[posicion] = " "

            if amenaza_rival:
                prioridad = 1
            elif posicion in CENTRO:
                prioridad = 2
            elif posicion in ESQUINAS:
                prioridad = 3
            else:
                prioridad = 4

        movimientos.append((prioridad, posicion))

    movimientos.sort()
    return [posicion for _, posicion in movimientos]


def minimax(tablero, maximizando, profundidad=0, alpha=-inf, beta=inf,
            memoria=None, estadisticas=None):
    """Devuelve la puntuación óptima mediante alfa-beta y memoria.

    O maximiza; X minimiza. La memoria guarda resultados exactos y cotas
    inferiores/superiores para reutilizar posiciones ya examinadas.
    """
    if memoria is None:
        memoria = {}
    if estadisticas is None:
        estadisticas = {"nodos": 0, "podas": 0, "aciertos_memoria": 0}

    estadisticas["nodos"] += 1

    ganador = hay_ganador(tablero)
    if ganador == "O":
        return 10 - profundidad
    if ganador == "X":
        return profundidad - 10
    if hay_empate(tablero):
        return 0

    alpha_original = alpha
    beta_original = beta
    clave = clave_tablero(tablero, maximizando, profundidad)
    entrada = memoria.get(clave)

    if entrada is not None:
        puntuacion, tipo = entrada
        estadisticas["aciertos_memoria"] += 1

        if tipo == "EXACTA":
            return puntuacion
        if tipo == "INFERIOR":
            alpha = max(alpha, puntuacion)
        elif tipo == "SUPERIOR":
            beta = min(beta, puntuacion)

        if alpha >= beta:
            return puntuacion

    jugador = "O" if maximizando else "X"
    movimientos = ordenar_movimientos(tablero, jugador)

    if maximizando:
        mejor_puntuacion = -inf

        for posicion in movimientos:
            tablero[posicion] = "O"
            puntuacion = minimax(
                tablero, False, profundidad + 1, alpha, beta,
                memoria, estadisticas
            )
            tablero[posicion] = " "

            mejor_puntuacion = max(mejor_puntuacion, puntuacion)
            alpha = max(alpha, mejor_puntuacion)

            if alpha >= beta:
                estadisticas["podas"] += 1
                break
    else:
        mejor_puntuacion = inf

        for posicion in movimientos:
            tablero[posicion] = "X"
            puntuacion = minimax(
                tablero, True, profundidad + 1, alpha, beta,
                memoria, estadisticas
            )
            tablero[posicion] = " "

            mejor_puntuacion = min(mejor_puntuacion, puntuacion)
            beta = min(beta, mejor_puntuacion)

            if alpha >= beta:
                estadisticas["podas"] += 1
                break

    if mejor_puntuacion <= alpha_original:
        tipo = "SUPERIOR"
    elif mejor_puntuacion >= beta_original:
        tipo = "INFERIOR"
    else:
        tipo = "EXACTA"

    memoria[clave] = (mejor_puntuacion, tipo)
    return mejor_puntuacion


def mejor_movimiento(tablero, devolver_estadisticas=False):
    """Encuentra la mejor casilla para O y reutiliza memoria en toda la jugada."""
    memoria = {}
    estadisticas = {"nodos": 0, "podas": 0, "aciertos_memoria": 0}
    mejor_puntuacion = -inf
    mejor_posicion = None
    alpha = -inf

    for posicion in ordenar_movimientos(tablero, "O"):
        tablero[posicion] = "O"
        puntuacion = minimax(
            tablero, False, 1, alpha, inf, memoria, estadisticas
        )
        tablero[posicion] = " "

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_posicion = posicion

        alpha = max(alpha, mejor_puntuacion)

    if devolver_estadisticas:
        estadisticas["puntuacion"] = mejor_puntuacion
        return mejor_posicion, estadisticas
    return mejor_posicion


def movimiento_maquina(tablero):
    posicion, estadisticas = mejor_movimiento(tablero, devolver_estadisticas=True)

    if posicion is not None:
        tablero[posicion] = "O"
        print("La máquina ha elegido la casilla:", posicion + 1)
        print(
            "Análisis: "
            f"{estadisticas['nodos']} nodos, "
            f"{estadisticas['podas']} podas y "
            f"{estadisticas['aciertos_memoria']} reutilizaciones de memoria."
        )


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
            print("¡Has ganado!" if ganador == "X" else "¡La máquina ha ganado!")
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
