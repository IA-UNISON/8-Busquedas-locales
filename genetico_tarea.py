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

__author__ = 'Daniel Eduardo Alvarez Terrazas'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """

    def __init__(self, problema, n_población,prob_muta=0.05, k=2):
        """
        Aqui puedes poner algunos de los parámetros
        que quieras utilizar en tu clase

        Para esta tarea vamos a cambiar la forma de representación
        para que se puedan utilizar operadores clásicos (esto implica
        reescribir los métodos estáticos cadea_a_estado y
        estado_a_cadena).

        """

        self.prob_muta = prob_muta
        self.k = k

        self.nombre = 'propuesto por el alumno (pmx + rotacion)'

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

        return 1.0 / (1.0 + (self.k * self.problema.costo(self.cadena_a_estado(individuo))))

    def selección(self):
        """
        Seleccion de estados mediante método diferente a la ruleta

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """

        parejas = []

        for _ in range(self.n_población):

            torneo1 = random.sample(range(self.n_población), 3)
            torneo2 = random.sample(range(self.n_población), 3)

            padre1 = max(
                torneo1,
                key=lambda i: self.población[i][0]
            )

            padre2 = max(
                torneo2,
                key=lambda i: self.población[i][0]
            )

            parejas.append((padre1, padre2))

        return parejas

    def cruza_individual(self, cadena1, cadena2):
        """

        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo

        """

        size = len(cadena1)

        p1 = [0] * size
        p2 = [0] * size

        for i in range(size):
            p1[i] = cadena1[i]
            p2[i] = cadena2[i]

        corte1 = random.randint(0, size - 2)
        corte2 = random.randint(corte1 + 1, size - 1)

        hijo = [None] * size

        # copiar segmento del padre 1

        hijo[corte1:corte2 + 1] = p1[corte1:corte2 + 1]

        # mapear genes del padre 2

        for i in range(corte1, corte2 + 1):

            if p2[i] not in hijo:

                pos = i

                while corte1 <= pos <= corte2:

                    val_p1 = p1[pos]
                    pos = p2.index(val_p1)

                hijo[pos] = p2[i]

        # llenar espacios restantes

        for i in range(size):

            if hijo[i] is None:
                hijo[i] = p2[i]

        return hijo

    def mutación(self, individuos):
        """

        @param poblacion: Una lista de individuos (listas).

        @return: None, es efecto colateral mutando los individuos
                 en la misma lista

        """

        for individuo in individuos:

            if random.random() < self.prob_muta:

                i = random.randint(0, len(individuo) - 1)
                j = random.randint(0, len(individuo) - 1)

                individuo[i], individuo[j] = (
                    individuo[j],
                    individuo[i]
                )

    def reemplazo_generacional(self, individuos):
        """
        Realiza el reemplazo generacional diferente al elitismo

        @param individuos: Una lista de cromosomas de hijos que pueden
                           usarse en el reemplazo
        @return: None (todo lo cambia internamente)

        Por default usamos solo el elitismo de conservar al mejor, solo si es
        mejor que lo que hemos encontrado hasta el momento.

        """

        reemplazo = [
            (self.adaptación(ind), ind)
            for ind in individuos
        ]

        # conservar al mejor padre

        reemplazo.append(max(self.población))

        # ordenar de mejor a peor

        reemplazo.sort(reverse=True)

        self.población = reemplazo[:self.n_población]


if __name__ == "__main__":
    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1

    g_propio = GeneticoPermutacionesPropio(genetico.ProblemaTonto(10), 10)
    genetico.prueba(g_propio)

