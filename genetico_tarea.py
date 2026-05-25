#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
genetico_tarea.py
-----------------

Algoritmo genético propio para problemas de permutaciones.
"""

import random
import genetico

__author__ = 'Rosario Luna Ortiz'


class GeneticoPermutacionesPropio(genetico.Genetico):

    def __init__(self,
                 problema,
                 n_población,
                 prob_mutacion=0.1):

        self.nombre = 'Genético propio'
        self.prob_mutacion = prob_mutacion

        super().__init__(problema, n_población)

    @staticmethod
    def estado_a_cadena(estado):

        return list(estado)

    @staticmethod
    def cadena_a_estado(cadena):

        return tuple(cadena)

    def adaptación(self, individuo):

        estado = self.cadena_a_estado(individuo)

        costo = self.problema.costo(estado)

        return 1 / (1 + costo)

    def selección(self):

        seleccionados = []

        for _ in range(self.n_población):

            a = random.randint(
                0,
                self.n_población - 1
            )

            b = random.randint(
                0,
                self.n_población - 1
            )

            if self.adaptación(self.población[a][1]) > \
               self.adaptación(self.población[b][1]):

                seleccionados.append(a)

            else:
                seleccionados.append(b)

        return [
            (seleccionados[i],
             seleccionados[i + 1])

            for i in range(
                0,
                len(seleccionados) - 1,
                2
            )
        ]

    def cruza_individual(self,
                         cadena1,
                         cadena2):

        n = len(cadena1)

        inicio = random.randint(0, n - 2)

        fin = random.randint(inicio + 1, n - 1)

        hijo = [-1] * n

        hijo[inicio:fin] = cadena1[inicio:fin]

        faltantes = [
            x for x in cadena2
            if x not in hijo
        ]

        indice = 0

        for i in range(n):

            if hijo[i] == -1:

                hijo[i] = faltantes[indice]

                indice += 1

        return hijo

    def mutación(self, individuos):

        for individuo in individuos:

            if random.random() < self.prob_mutacion:

                i, j = random.sample(
                    range(len(individuo)),
                    2
                )

                individuo[i], individuo[j] = \
                    individuo[j], individuo[i]

    def reemplazo_generacional(self, individuos):

        hijos = [
            (self.adaptación(individuo), individuo)
            for individuo in individuos
        ]

        nueva = self.población + hijos

        nueva.sort(reverse=True)

        self.población = nueva[:self.n_población]

# ============================================================
# DESCRIPCIÓN DEL ALGORITMO GENÉTICO PROPUESTO
# ============================================================

# El algoritmo implementado utiliza:
#
# - Selección por torneo.
# - Cruza tipo Order Crossover (OX).
# - Mutación por intercambio de posiciones.
# - Reemplazo generacional basado en adaptación.
#
# Este enfoque mantiene soluciones válidas para problemas
# de permutaciones como N-Reinas y evita cromosomas inválidos.
#
# La selección por torneo permitió mantener presión selectiva
# sin perder demasiada diversidad genética.
#
# La cruza OX conservó subsecuencias válidas de los padres.
#
# La mutación ayudó a evitar convergencia prematura.
if __name__ == "__main__":

    g_propio = GeneticoPermutacionesPropio(
        genetico.ProblemaTonto(10),
        10
    )

    genetico.prueba(g_propio)