"""Compara Minimax clásico con la IA optimizada del proyecto.

Ejecuta: python comparar_algoritmos.py
"""

from time import perf_counter

from main import hay_ganador, hay_empate, mejor_movimiento


def minimax_clasico(tablero, maximizando, profundidad, contador):
    """Versión de referencia sin poda alfa-beta ni memoria."""
    contador[0] += 1
    ganador = hay_ganador(tablero)

    if ganador == "O":
        return 10 - profundidad
    if ganador == "X":
        return profundidad - 10
    if hay_empate(tablero):
        return 0

    simbolo = "O" if maximizando else "X"
    puntuaciones = []

    for posicion in range(9):
        if tablero[posicion] == " ":
            tablero[posicion] = simbolo
            puntuaciones.append(
                minimax_clasico(tablero, not maximizando, profundidad + 1, contador)
            )
            tablero[posicion] = " "

    return max(puntuaciones) if maximizando else min(puntuaciones)


def probar_minimax_clasico(tablero):
    contador = [0]
    mejor_puntuacion = float("-inf")
    mejor_posicion = None
    inicio = perf_counter()

    for posicion in range(9):
        if tablero[posicion] == " ":
            tablero[posicion] = "O"
            puntuacion = minimax_clasico(tablero, False, 1, contador)
            tablero[posicion] = " "

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_posicion = posicion

    return mejor_posicion, mejor_puntuacion, contador[0], perf_counter() - inicio


def main():
    tablero = [" "] * 9

    print("COMPARACIÓN DE MINIMAX")
    print("=" * 42)

    posicion, puntuacion, nodos, tiempo = probar_minimax_clasico(tablero)
    print("MINIMAX CLÁSICO")
    print(f"  Mejor casilla: {posicion + 1}")
    print(f"  Puntuación:    {puntuacion}")
    print(f"  Nodos:         {nodos:,}")
    print(f"  Tiempo:        {tiempo:.6f} s\\n")

    inicio = perf_counter()
    posicion_optima, estadisticas = mejor_movimiento(
        tablero, devolver_estadisticas=True
    )
    tiempo_optimo = perf_counter() - inicio

    print("MINIMAX OPTIMIZADO")
    print(f"  Mejor casilla: {posicion_optima + 1}")
    print(f"  Puntuación:    {estadisticas['puntuacion']}")
    print(f"  Nodos:         {estadisticas['nodos']:,}")
    print(f"  Podas:         {estadisticas['podas']:,}")
    print(f"  Aciertos memoria: {estadisticas['aciertos_memoria']:,}")
    print(f"  Tiempo:        {tiempo_optimo:.6f} s\\n")

    reduccion = (1 - estadisticas["nodos"] / nodos) * 100
    misma_puntuacion = puntuacion == estadisticas["puntuacion"]

    print("RESULTADO")
    print("-" * 42)
    print(f"¿Misma puntuación óptima?: {'Sí' if misma_puntuacion else 'No'}")
    print(f"Reducción de nodos:         {reduccion:.2f}%")
    print("\\nLos tiempos dependen del ordenador y de la carga del sistema.")


if __name__ == "__main__":
    main()
