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
    #
    #       - N = 8:   n_poblacion = 64,   generaciones = 100,  prob_mutacion = 0.10  (Exito: 100%, 0.17s)
    #       - N = 16:  n_poblacion = 100,  generaciones = 150,  prob_mutacion = 0.08  (Exito: 100%, 0.77s)
    #       - N = 32:  n_poblacion = 256,  generaciones = 400,  prob_mutacion = 0.10  (Exito: 100%, 9.77s)
    #       - N = 64:  n_poblacion = 512,  generaciones = 800,  prob_mutacion = 0.10  (Exito: 100%, 76.57s)
    #       - N = 128: n_poblacion = 1024, generaciones = 1500, prob_mutacion = 0.10  (Exito: 60%, 569.28s)
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun
    #       tu experiencia?
    #
    #       1. El tamaño de la población y el número de generaciones deben escalar
    #          exponencialmente con N porque la selección por ruleta tiene baja presión
    #          selectiva cuando las aptitudes del grupo son similares.
    #       2. La mutación debe ser relativamente alta (8%-10%) para inyectar diversidad
    #          y contrarrestar la convergencia prematura.
    #

    n_poblacion = 100
    generaciones = 150
    prob_mutacion = 0.08

    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(16),
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
    #       (escribelos abajo de esta linea)
    #
    #       - N = 8:   n_poblacion = 30,  generaciones = 40,   prob_mutacion = 0.05  (Exito: 100%, 0.05s)
    #       - N = 16:  n_poblacion = 60,  generaciones = 80,   prob_mutacion = 0.05  (Exito: 100%, 0.31s)
    #       - N = 32:  n_poblacion = 100, generaciones = 150,  prob_mutacion = 0.05  (Exito: 100%, 2.12s)
    #       - N = 64:  n_poblacion = 300, generaciones = 400,  prob_mutacion = 0.08  (Exito: 100%, 32.57s)
    #       - N = 128: n_poblacion = 800, generaciones = 1000, prob_mutacion = 0.10  (Exito: 100%, 421.57s)
    #
    #   -- ¿Que reglas podrías establecer para asignar valores
    #       segun tu experiencia?
    #
    #       1. El uso de la codificación de Lehmer (que siempre produce soluciones válidas tras la cruza)
    #          junto con Selección por Torneo (k=3) reduce drásticamente la población requerida (aprox. la mitad).
    #          y el número de generaciones necesarias para converger.
    #       2. Un esquema de reemplazo generacional con élite (10% de los mejores padres) conserva el
    #          progreso sin degradación de la aptitud, lo que da 100% de éxito en tableros grandes (como N=128)
    #          que el algoritmo original no lograba resolver confiablemente.
    #