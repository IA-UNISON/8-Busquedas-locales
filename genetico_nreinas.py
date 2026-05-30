#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba de los algoritmos genéticos utilizando el problema
de las n-reinas para aprender a ajustarlos y probarlos.

"""

from time import time
from itertools import combinations
from random import shuffle
import genetico
import genetico_tarea

__author__ = 'Daniel Eduardo Alvarez Terrazas'

class ProblemaNreinas(genetico.Problema):
    """
    Las N reinas para AG

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        return sum([1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)])


def prueba_genetico(algo_genetico, n_generaciones):
    """
    ejecuta una prueba del algoritmo genetico
    """

    t_inicial = time()

    solucion = algo_genetico.busqueda(n_generaciones)

    t_final = time()

    costo = algo_genetico.problema.costo(solucion)

    return costo, t_final - t_inicial

def automatizar_pruebas():

    # pruebas para el algoritmo del profesor

    pruebas_profe = [

    (8, 100, 100, 0.03),

    (16, 100, 150, 0.04),

    (32, 120, 300, 0.02),

    (64, 150, 500, 0.02),

    (128, 180, 700, 0.02)

    ]   


    print("\n" + "=" * 65)
    print(" ALGORITMO DEL PROFESOR (GENETICO PERMUTACIONES)")
    print("=" * 65)

    print(
        f"{'reinas':<10}"
        f"{'poblacion':<15}"
        f"{'generaciones':<18}"
        f"{'mutacion':<12}"
        f"{'tiempo(s)':<12}"
        f"{'costo':<8}"
    )

    print("-" * 65)

    for r, pob, gen, mut in pruebas_profe:

        alg_gen = genetico.GeneticoPermutaciones(

            ProblemaNreinas(r),

            pob,

            mut
        )

        c, t = prueba_genetico(alg_gen, gen)

        print(
            f"{r:<10}"
            f"{pob:<15}"
            f"{gen:<18}"
            f"{mut:<12.2f}"
            f"{t:<12.2f}"
            f"{c:<8}"
        )

    # pruebas para el algoritmo propuesto

    pruebas_propio = [

        (8, 80, 120, 0.03),

        (16, 80, 180, 0.04),

        (32, 100, 300, 0.05),

        (64, 120, 500, 0.06),

        (128, 150, 700, 0.07)

    ]


    print("\n" + "=" * 65)
    print(" ALGORITMO PROPUESTO (PMX + ROTACION)")
    print("=" * 65)

    print(
        f"{'reinas':<10}"
        f"{'poblacion':<15}"
        f"{'generaciones':<18}"
        f"{'mutacion':<12}"
        f"{'tiempo(s)':<12}"
        f"{'costo':<8}"
    )

    print("-" * 65)

    for r, pob, gen, mut in pruebas_propio:

        alg_propio = genetico_tarea.GeneticoPermutacionesPropio(

            ProblemaNreinas(r),

            pob,

            mut
        )

        c, t = prueba_genetico(alg_propio, gen)

        print(
            f"{r:<10}"
            f"{pob:<15}"
            f"{gen:<18}"
            f"{mut:<12.2f}"
            f"{t:<12.2f}"
            f"{c:<8}"
        )



if __name__ == "__main__":

    automatizar_pruebas()

    # Modifica los parámetro del algoritmo genetico que propuso el
    # profesor (el cual se conoce como genetico.GeneticoPermutaciones)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima,
    # utilizando el menor tiempo posible en promedio. Realiza esto
    # para las 8, 16, 32, 64 y 128 reinas.
    #
    # Lo que puedes modificar es el tamaño de la población, el número
    # de generaciones y/o la probabilidad de mutación.
    #
    # Recuerda que podrias automatizar el problema haciendo una
    # función que genere una tabla con las soluciones, o hazlo a mano
    # si eso ayuda a comprender mejor el algoritmo.
    #
    #   -- ¿Cuales son en cada caso los mejores valores?  (escribelos
    #       abajo de esta linea)
    #  n = 8:   poblacion = 100, generaciones = 100, prob_mutacion = 0.03, tiempo = 0.12s, costo = 0
    #  n = 16:  poblacion = 100, generaciones = 150, prob_mutacion = 0.04, tiempo = 0.27s, costo = 0
    #  n = 32:  poblacion = 120, generaciones = 300, prob_mutacion = 0.02, tiempo = 1.65s, costo = 0
    #  n = 64:  poblacion = 150, generaciones = 500, prob_mutacion = 0.02, tiempo = 11.39s, costo = 3
    #  n = 128: poblacion = 180, generaciones = 700, prob_mutacion = 0.02, tiempo = 75.99s, costo = 25
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun
    #       tu experiencia?
    #
    # 1. conforme aumenta el numero de reinas, fue necesario aumentar
    # principalmente el numero de generaciones para que el algoritmo
    # tuviera mas tiempo de converger a mejores soluciones.
    #
    # 2. el tamaño de la poblacion tambien tuvo que aumentar, aunque de
    # manera moderada, ya que poblaciones demasiado grandes aumentaban
    # mucho el tiempo de ejecucion sin mejorar demasiado los resultados.
    #
    # 3. las probabilidades de mutacion mas bajas funcionaron mejor para
    # tableros grandes, ya que mutaciones muy altas destruian soluciones
    # buenas y hacian mas dificil la convergencia.


    # Modifica los parámetro del algoritmo genetico que propusite tu
    # mismo (el cual se conoce como
    # genetico_tarea.GeneticoPermutacionesPropio). De ser muchos
    # parámetros, restringete a 2 o 3, buscando que el algoritmo
    # encuentre SIEMPRE una solución óptima, utilizando el menor
    # tiempo posible en promedio. Realiza esto para las 8, 16, 32, 64 y 128
    # reinas.
    #
    #   -- ¿Cuales son en cada caso los mejores valores?
    #       (escribelos abajo de esta linea)
    #  n = 8:   poblacion = 80,  generaciones = 120, prob_mutacion = 0.03, tiempo = 0.08s, costo = 0
    #  n = 16:  poblacion = 80,  generaciones = 180, prob_mutacion = 0.04, tiempo = 0.23s, costo = 0
    #  n = 32:  poblacion = 100, generaciones = 300, prob_mutacion = 0.05, tiempo = 1.27s, costo = 0
    #  n = 64:  poblacion = 120, generaciones = 500, prob_mutacion = 0.06, tiempo = 8.76s, costo = 1
    #  n = 128: poblacion = 150, generaciones = 700, prob_mutacion = 0.07, tiempo = 58.44s, costo = 2
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores
    #       segun tu experiencia?
    #
    # 1. el algoritmo propuesto necesito menos poblacion que el algoritmo
    # del profesor, ya que la cruza pmx y la seleccion por torneo
    # mantuvieron mejor la diversidad genetica.
    #
    # 2. conforme aumentaba el tamaño del tablero, fue necesario aumentar
    # las generaciones y ligeramente la mutacion para evitar que el
    # algoritmo se estancara en optimos locales.
    #
    # 3. una mutacion demasiado baja hacia que la poblacion se volviera
    # muy parecida entre si, mientras que una mutacion demasiado alta
    # destruia soluciones buenas. por eso los mejores resultados se
    # obtuvieron aumentando la mutacion poco a poco.
    #
    # 4. en general el algoritmo propuesto obtuvo mejores resultados en
    # menos tiempo para tableros grandes, especialmente en 64 y 128 reinas.



