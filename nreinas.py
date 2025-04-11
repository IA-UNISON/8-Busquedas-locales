#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
from random import shuffle
from random import sample
from itertools import combinations


class ProblemaNreinas(blocales.Problema):
    """
    Las N reinas en forma de búsqueda local 
    
    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        """
        Una lista de valores, ordenados al azar
        
        """
        estado = list(range(1, self.n + 1))
        shuffle(estado)
        return tuple(estado)

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        """
        x = list(estado)
        for i, j in combinations(range(self.n), 2):
            x[i], x[j] = x[j], x[i]
            yield tuple(x)
            x[i], x[j] = x[j], x[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        """
        return sum(
            abs(estado[i] - estado[j]) == abs(i - j)
            for (i, j) in combinations(range(self.n), 2)
        )


def prueba_descenso_colinas(pbl=ProblemaNreinas(8), rep=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center(10) + "costo".center(10))
    
    c = 1e10
    for intento in range(rep):
        solucion = blocales.descenso_colinas(pbl)
        c_intento = pbl.costo(solucion)
        print(str(intento).center(10) +
              str(c_intento).center(10))
        if c_intento < c:
            mejor_solucion = solucion
            c = c_intento
    print("\n\nEl mejor estado encontrado es:")
    print(mejor_solucion)


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


if __name__ == "__main__":

    prueba_descenso_colinas(ProblemaNreinas(50), 10)
    prueba_temple_simulado(ProblemaNreinas(50))

