"""Pruebas exhaustivas para comprobar que la IA sigue jugando óptimamente.

Ejecuta desde la carpeta del proyecto:
    python -m unittest -v

Se recorren todas las posiciones legales alcanzables desde una partida vacía
y se compara el resultado de la IA optimizada con un Minimax de referencia.
"""

import unittest

from main import hay_ganador, hay_empate, minimax


def minimax_referencia(tablero, maximizando, profundidad):
    """Minimax sin poda ni memoria: referencia independiente para las pruebas."""
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
                minimax_referencia(tablero, not maximizando, profundidad + 1)
            )
            tablero[posicion] = " "

    return max(puntuaciones) if maximizando else min(puntuaciones)


def posiciones_legales():
    """Genera una vez cada estado legal alcanzable, junto con el turno y profundidad."""
    inicial = [" "] * 9
    pendientes = [(inicial, True, 0)]
    visitadas = set()

    while pendientes:
        tablero, maximizando, profundidad = pendientes.pop()
        clave = (tuple(tablero), maximizando)

        if clave in visitadas:
            continue
        visitadas.add(clave)
        yield tablero, maximizando, profundidad

        if hay_ganador(tablero) is not None or hay_empate(tablero):
            continue

        simbolo = "O" if maximizando else "X"
        for posicion in range(9):
            if tablero[posicion] == " ":
                siguiente = tablero.copy()
                siguiente[posicion] = simbolo
                pendientes.append((siguiente, not maximizando, profundidad + 1))


class PruebasMinimaxOptimizado(unittest.TestCase):

    def test_resultados_iguales_al_minimax_de_referencia(self):
        cantidad = 0

        for tablero, maximizando, profundidad in posiciones_legales():
            esperado = minimax_referencia(
                tablero.copy(), maximizando, profundidad
            )
            estadisticas = {
                "nodos": 0,
                "podas": 0,
                "aciertos_memoria": 0,
            }
            obtenido = minimax(
                tablero.copy(),
                maximizando,
                profundidad,
                memoria={},
                estadisticas=estadisticas,
            )

            self.assertEqual(
                obtenido,
                esperado,
                msg=f"Resultado distinto en la posición {tablero}",
            )
            cantidad += 1

        self.assertGreater(cantidad, 0)
        print(f"\\nPosiciones legales comprobadas: {cantidad}")

    def test_ia_puede_forzar_al_menos_empate_con_cualquier_salida_humana(self):
        from main import mejor_movimiento

        # X empieza. Para cada una de sus nueve posibles salidas,
        # comprobamos que la respuesta óptima de O no permite una derrota.
        for primera_jugada_x in range(9):
            tablero = [" "] * 9
            tablero[primera_jugada_x] = "X"

            posicion_o = mejor_movimiento(tablero)
            self.assertIsNotNone(posicion_o)
            tablero[posicion_o] = "O"

            resultado = minimax_referencia(tablero, False, 2)
            self.assertGreaterEqual(
                resultado,
                0,
                msg=f"La IA podría perder tras la salida X en {primera_jugada_x + 1}",
            )


if __name__ == "__main__":
    unittest.main()
