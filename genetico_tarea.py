#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genetico_tarea.py
-----------------

En este módulo vas a desarrollar tu propio algoritmo
genético para resolver problemas de permutaciones

"""

import random
import genetico

__author__ = 'Kevin Nunez'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """

    def __init__(self, problema, n_población):
        self.nombre = 'propuesto por el alumno'
        self.prob_muta = 0.05
        super().__init__(problema, n_población)

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas independiente
        del problema de permutación

        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres

        """
        return list(estado)

    @staticmethod
    def cadena_a_estado(cadena):
        """
        Convierte una cadena de cromosomas a un estado donde el estado es
        una posible solución a un problema de permutaciones

        @param cadena: Una lista de cromosomas o valores
        @return: Una tupla con un estado válido

        """
        return tuple(cadena)

    def adaptación(self, individuo):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado
        mejor, mayor costo, menor adaptción.

        @param individuo: Una lista de cromosomas
        @return un número con la adaptación del individuo

        """
        return 1.0 / (1.0 + self.problema.costo(self.cadena_a_estado(individuo)))

    def selección(self):
        """
        Seleccion por torneo. Se eligen k candidatos al azar y gana
        el de mayor adaptación. Más eficiente que la ruleta.

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """
        k = 3
        parejas = []
        for _ in range(self.n_población):
            candidatos_i = random.sample(range(len(self.población)), k)
            i = max(candidatos_i, key=lambda x: self.población[x][0])
            candidatos_j = random.sample(range(len(self.población)), k)
            j = max(candidatos_j, key=lambda x: self.población[x][0])
            parejas.append((i, j))
        return parejas

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza por orden (OX). Copia un segmento de cadena1 y completa
        con el orden relativo de cadena2. Mantiene la propiedad de permutación.

        @param cadena1: Una lista con un individuo
        @param cadena2: Una lista con otro individuo
        @return: Un individuo nuevo

        """
        n = len(cadena1)
        hijo = [None] * n
        inicio = random.randint(0, n - 1)
        fin = random.randint(inicio + 1, n)
        hijo[inicio:fin] = cadena1[inicio:fin]
        pos = fin % n
        for gen in cadena2[fin:] + cadena2[:fin]:
            if gen not in hijo:
                hijo[pos] = gen
                pos = (pos + 1) % n
        return hijo

    def mutación(self, individuos):
        """
        Mutación por intercambio. Con probabilidad prob_muta intercambia
        dos posiciones aleatorias del individuo.

        @param individuos: Una lista de individuos (listas).
        @return: None, es efecto colateral mutando los individuos
                 en la misma lista

        """
        for individuo in individuos:
            for i in range(len(individuo)):
                if random.random() < self.prob_muta:
                    j = random.randint(0, len(individuo) - 1)
                    individuo[i], individuo[j] = individuo[j], individuo[i]

    def reemplazo_generacional(self, individuos):
        """
        Reemplazo generacional: se mezclan padres e hijos y se conservan
        los mejores. Diferente al elitismo puro porque los hijos pueden
        desplazar a cualquier padre, no solo al peor.

        @param individuos: Una lista de cromosomas de hijos
        @return: None (todo lo cambia internamente)

        """
        hijos_evaluados = [(self.adaptación(ind), ind) for ind in individuos]
        todos = self.población + hijos_evaluados
        todos.sort(reverse=True)
        self.población = todos[:self.n_población]


if __name__ == "__main__":
    g_propio = GeneticoPermutacionesPropio(genetico.ProblemaTonto(10), 10)
    genetico.prueba(g_propio)

