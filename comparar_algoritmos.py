"""Compara Minimax y Minimax con poda alfa-beta en el tres en raya.

Ejecuta: python comparar_algoritmos.py
No modifica main.py: es un experimento independiente.
"""

from time import perf_counter


COMBINACIONES_GANADORAS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

CENTRO = (4,)
ESQUINAS = (0, 2, 6, 8)
LATERALES = (1, 3, 5, 7)


def hay_ganador(tablero):
    for a, b, c in COMBINACIONES_GANADORAS:
        if tablero[a] != " " and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]
    return None


def hay_empate(tablero):
    return " " not in tablero and hay_ganador(tablero) is None


def ordenar_movimientos(tablero, jugador):
    """Prioriza ganar, bloquear, centro, esquinas y finalmente laterales."""
    rival = "X" if jugador == "O" else "O"
    movimientos = []

    for posicion in range(9):
        if tablero[posicion] != " ":
            continue

        # Una victoria inmediata siempre tiene la máxima prioridad.
        tablero[posicion] = jugador
        gana = hay_ganador(tablero) == jugador
        tablero[posicion] = " "
        if gana:
            prioridad = 0
        else:
            # Si el rival ganaría ocupando esta casilla, conviene bloquear.
            tablero[posicion] = rival
            rival_gana = hay_ganador(tablero) == rival
            tablero[posicion] = " "
            if rival_gana:
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


def minimax(tablero, maximizando, profundidad, contador):
    """Minimax original: explora todas las continuaciones posibles."""
    contador[0] += 1
    ganador = hay_ganador(tablero)

    if ganador == "O":
        return 10 - profundidad
    if ganador == "X":
        return profundidad - 10
    if hay_empate(tablero):
        return 0

    if maximizando:
        mejor = float("-inf")
        for posicion in range(9):
            if tablero[posicion] == " ":
                tablero[posicion] = "O"
                puntuacion = minimax(tablero, False, profundidad + 1, contador)
                tablero[posicion] = " "
                mejor = max(mejor, puntuacion)
        return mejor

    mejor = float("inf")
    for posicion in range(9):
        if tablero[posicion] == " ":
            tablero[posicion] = "X"
            puntuacion = minimax(tablero, True, profundidad + 1, contador)
            tablero[posicion] = " "
            mejor = min(mejor, puntuacion)
    return mejor


def minimax_alfa_beta(tablero, maximizando, profundidad, alpha, beta, contador):
    """Minimax con poda y ordenación heurística de movimientos."""
    contador[0] += 1
    ganador = hay_ganador(tablero)

    if ganador == "O":
        return 10 - profundidad
    if ganador == "X":
        return profundidad - 10
    if hay_empate(tablero):
        return 0

    jugador = "O" if maximizando else "X"
    movimientos = ordenar_movimientos(tablero, jugador)

    if maximizando:
        mejor = float("-inf")
        for posicion in movimientos:
            tablero[posicion] = "O"
            puntuacion = minimax_alfa_beta(
                tablero, False, profundidad + 1, alpha, beta, contador
            )
            tablero[posicion] = " "
            mejor = max(mejor, puntuacion)
            alpha = max(alpha, mejor)

            if beta <= alpha:
                break
        return mejor

    mejor = float("inf")
    for posicion in movimientos:
        tablero[posicion] = "X"
        puntuacion = minimax_alfa_beta(
            tablero, True, profundidad + 1, alpha, beta, contador
        )
        tablero[posicion] = " "
        mejor = min(mejor, puntuacion)
        beta = min(beta, mejor)

        if beta <= alpha:
            break
    return mejor


def mejor_jugada(algoritmo, tablero):
    """Calcula la mejor jugada de O y devuelve posición, puntuación y nodos."""
    mejor_posicion = None
    mejor_puntuacion = float("-inf")
    contador = [0]

    if algoritmo == "minimax":
        movimientos = [p for p in range(9) if tablero[p] == " "]
    else:
        movimientos = ordenar_movimientos(tablero, "O")

    for posicion in movimientos:
        tablero[posicion] = "O"

        if algoritmo == "minimax":
            puntuacion = minimax(tablero, False, 1, contador)
        else:
            puntuacion = minimax_alfa_beta(
                tablero, False, 1, float("-inf"), float("inf"), contador
            )

        tablero[posicion] = " "

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_posicion = posicion

    return mejor_posicion, mejor_puntuacion, contador[0]


def ejecutar_prueba(nombre, algoritmo, tablero):
    inicio = perf_counter()
    posicion, puntuacion, nodos = mejor_jugada(algoritmo, tablero.copy())
    tiempo = perf_counter() - inicio

    print(f"{nombre}:")
    print(f"  Mejor casilla: {posicion + 1 if posicion is not None else 'ninguna'}")
    print(f"  Puntuación:    {puntuacion}")
    print(f"  Nodos:         {nodos:,}")
    print(f"  Tiempo:        {tiempo:.6f} segundos")
    print()

    return puntuacion, nodos, tiempo


def main():
    tablero = [" "] * 9

    print("COMPARACIÓN DE ALGORITMOS - TRES EN RAYA")
    print("=" * 43)
    print("Posición inicial: tablero vacío\n")

    resultado_minimax = ejecutar_prueba("MINIMAX", "minimax", tablero)
    resultado_poda = ejecutar_prueba(
        "MINIMAX + ALFA-BETA + ORDENACIÓN", "alfa_beta", tablero
    )

    puntuacion_igual = resultado_minimax[0] == resultado_poda[0]
    reduccion = (1 - resultado_poda[1] / resultado_minimax[1]) * 100

    print("RESULTADO")
    print("-" * 43)
    print(f"¿Misma puntuación óptima?: {'Sí' if puntuacion_igual else 'No'}")
    print(f"Reducción de nodos:         {reduccion:.2f}%")
    print(f"Factor de nodos:            {resultado_minimax[1] / resultado_poda[1]:.2f}x")
    print("\nNota: el tiempo puede variar según el ordenador y la carga del sistema.")


if __name__ == "__main__":
    main()
