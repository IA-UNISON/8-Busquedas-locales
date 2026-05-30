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
import random

__author__ = 'juliowaissman'

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


def prueba_genetico(algo_genetico, n_generaciones, verbose=False):
    """
    Prueba de los algoritmos genéticos con el problema de las n reinas
    desarrollado para búsquedas locales (tarea 2).

    @param algo_genetico: objeto de la clase genetico.Genetico
    @param n_generaciones: Generaciones (iteraciones) del algortimo
    @param verbose: True si quieres desplegar informacion básica
    @return: Un estado con la solucion (una permutacion de range(n)

    """
    t_inicial = time()
    solucion = algo_genetico.busqueda(n_generaciones)
    t_final = time()
    if verbose:
        print("\nUtilizando el AG: {}".format(algo_genetico.nombre))
        print("Con poblacion de dimensión {}".format(
            algo_genetico.n_población))
        print("Con {} generaciones".format(n_generaciones))
        print("Costo de la solución encontrada: {}".format(
            algo_genetico.problema.costo(solucion)))
        print("Tiempo de ejecución en segundos: {}".format(
            t_final - t_inicial))
    return solucion


if __name__ == "__main__":
    random.seed(804)
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
    #   -- ¿Cuales son en cada caso los mejores valores?
    #  N = 8:   n_poblacion = 50,  generaciones = 80,  prob_mutacion = 0.05  (Costo: 0, Tiempo: 0.12s)
    #  N = 16:  n_poblacion = 100, generaciones = 150, prob_mutacion = 0.05  (Costo: 0, Tiempo: 1.21s)
    #  N = 32:  n_poblacion = 120, generaciones = 300, prob_mutacion = 0.02  (Costo: 0, Tiempo: 6.01s)
    #  N = 64:  n_poblacion = 150, generaciones = 500, prob_mutacion = 0.02  (Costo: 0, Tiempo: 38.97s)
    #  N = 128: n_poblacion = 300, generaciones = 500, prob_mutacion = 0.05  (Costo: 39, Tiempo: 315.32s)
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia?
    #   El algoritmo mantiene un buen rendimiento hasta tableros de tamaño N=64, pero en N=128 el espacio de búsqueda
    #   crece bastante, por lo que 300 individuos y 500 generaciones resultan insuficientes. Para estos tamaños se
    #   requiere aumentar significativamente la población y el número de generaciones para conservar la diversidad
    #   genética y mejorar la convergencia. Además, n tableros de tamaño medio (N=32 y N=64), una tasa de mutación más
    #   baja favorece la explotación de soluciones prometedoras, permitiendo que la cruza tenga mayor impacto y evitando
    #   introducir ruido excesivo en la búsqueda.

    n_poblacion = 50
    generaciones = 80
    prob_mutacion = 0.05
    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(8),
                                             n_poblacion, prob_mutacion)
    solucion = prueba_genetico(alg_gen, generaciones, True)

    n_poblacion = 100
    generaciones = 150
    prob_mutacion = 0.05
    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(16),
                                             n_poblacion, prob_mutacion)
    solucion = prueba_genetico(alg_gen, generaciones, True)

    n_poblacion = 120
    generaciones = 300
    prob_mutacion = 0.02
    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(32),
                                             n_poblacion, prob_mutacion)
    solucion = prueba_genetico(alg_gen, generaciones, True)

    n_poblacion = 150
    generaciones = 500
    prob_mutacion = 0.02
    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(64),
                                             n_poblacion, prob_mutacion)
    solucion = prueba_genetico(alg_gen, generaciones, True)

    n_poblacion = 300
    generaciones = 500
    prob_mutacion = 0.05
    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(128),
                                             n_poblacion, prob_mutacion)
    solucion = prueba_genetico(alg_gen, generaciones, True)

    # Modifica los parámetro del algoritmo genetico que propusite tu
    # mismo (el cual se conoce como
    # genetico_tarea.GeneticoPermutacionesPropio). De ser muchos
    # parámetros, restringete a 2 o 3, buscando que el algoritmo
    # encuentre SIEMPRE una solución óptima, utilizando el menor
    # tiempo posible en promedio. Realiza esto para las 8, 16, 32, 64 y 128
    # reinas.
    #
    #   -- ¿Cuales son en cada caso los mejores valores?
    #  N = 8:   n_poblacion = 50,  generaciones = 500,  (Costo: 0,  Tiempo: 0.21s)
    #  N = 16:  n_poblacion = 100, generaciones = 1500, (Costo: 1,  Tiempo: 2.91s)
    #  N = 32:  n_poblacion = 150, generaciones = 3000, (Costo: 6,  Tiempo: 30.50s)
    #  N = 64:  n_poblacion = 200, generaciones = 6000, (Costo: 18, Tiempo: 275.83s)
    #  N = 128: n_poblacion = 300, generaciones = 1200, (Costo: 49, Tiempo: 319.71s)
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia?
    #   La estrategia de cruza utilizada tiende a reducir rápidamente la variedad de soluciones en la población,
    #   limitando la capacidad de búsqueda local. Como consecuencia, el algoritmo depende en gran medida de los
    #   cataclismos para escapar del estancamiento y continuar explorando nuevas regiones del espacio de búsqueda. Otra
    #   regla importante a destacar es que a medida que aumenta el tamaño del problema, encontrar la solución óptima
    #   se vuelve muchísimo más difícil. Los resultados muestran que el algoritmo requiere una cantidad muy elevada de
    #   generaciones para converger, por lo que su desempeño en instancias grandes depende de una capacidad
    #   computacional significativamente mayor.

    n_poblacion_propia = 50
    generaciones_propia = 500
    generaciones_a_tolerar_propia = 8
    alg_gen_propio = genetico_tarea.GeneticoPermutacionesPropio(
        ProblemaNreinas(8),
        n_población=n_poblacion_propia,
        generaciones_a_tolerar=generaciones_a_tolerar_propia
    )
    solucion_propia = prueba_genetico(alg_gen_propio, generaciones_propia, True)

    n_poblacion_propia = 100
    generaciones_propia = 1500
    generaciones_a_tolerar_propia = 25
    alg_gen_propio = genetico_tarea.GeneticoPermutacionesPropio(
        ProblemaNreinas(16),
        n_población=n_poblacion_propia,
        generaciones_a_tolerar=generaciones_a_tolerar_propia
    )
    solucion_propia = prueba_genetico(alg_gen_propio, generaciones_propia, True)

    n_poblacion_propia = 150
    generaciones_propia = 3000
    generaciones_a_tolerar_propia = 35
    alg_gen_propio = genetico_tarea.GeneticoPermutacionesPropio(
        ProblemaNreinas(32),
        n_población=n_poblacion_propia,
        generaciones_a_tolerar=generaciones_a_tolerar_propia
    )
    solucion_propia = prueba_genetico(alg_gen_propio, generaciones_propia, True)

    n_poblacion_propia = 200
    generaciones_propia = 6000
    generaciones_a_tolerar_propia = 45
    alg_gen_propio = genetico_tarea.GeneticoPermutacionesPropio(
        ProblemaNreinas(64),
        n_población=n_poblacion_propia,
        generaciones_a_tolerar=generaciones_a_tolerar_propia
    )
    solucion_propia = prueba_genetico(alg_gen_propio, generaciones_propia, True)

    n_poblacion_propia = 300
    generaciones_propia = 1200
    generaciones_a_tolerar_propia = 60
    alg_gen_propio = genetico_tarea.GeneticoPermutacionesPropio(
        ProblemaNreinas(128),
        n_población=n_poblacion_propia,
        generaciones_a_tolerar=generaciones_a_tolerar_propia
    )
    solucion_propia = prueba_genetico(alg_gen_propio, generaciones_propia, True)