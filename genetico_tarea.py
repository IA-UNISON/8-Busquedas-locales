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

__author__ = 'Beltran Zazueta Emily'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self, problema, n_población, prob_muta=0.1):
        """
        Aqui puedes poner algunos de los parámetros
        que quieras utilizar en tu clase

        Para esta tarea vamos a cambiar la forma de representación
        para que se puedan utilizar operadores clásicos (esto implica
        reescribir los métodos estáticos cadea_a_estado y
        estado_a_cadena).

        """
        self.prob_muta = prob_muta
        self.nombre = 'propuesto por el alumno'
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
        return 1 / (1.0 + self.problema.costo(self.cadena_a_estado(individuo)))

    @staticmethod
    def _distancia(ind1, ind2):
        return sum(1 for a, b in zip(ind1, ind2) if a != b)

    def selección(self):
        """
        Selección basada en la diferencia entre individuos. Cuanta más
        diferencia haya entre dos individuos, mayor probabilidad tienen de
        reproducirse.

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """
        n = len(self.población)
        if n < 2:
            return []

        parejas = [(i, j) for i in range(n) for j in range(i + 1, n)]
        pesos = [self._distancia(self.población[i][1], self.población[j][1])
                 for (i, j) in parejas]
        suma = sum(pesos)
        if suma == 0:
            return [(random.randrange(n), random.randrange(n))
                    for _ in range(self.n_población)]

        return random.choices(parejas, weights=pesos, k=self.n_población)

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza especial para problemas de permutaciones.

        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo

        """
        hijo = cadena1[:]
        len_cadena = len(hijo)
        corte1 = random.randint(0, len_cadena - 1)
        corte2 = random.randint(corte1 + 1, len_cadena)
        evita = hijo[:corte1] + hijo[corte2:]
        for i in range(corte1, corte2):
            hijo[i] = cadena2[i]
            while hijo[i] in evita:
                hijo[i] = cadena2[cadena1.index(hijo[i])]
        return hijo

    def mutación(self, individuos, prob_muta=None):
        """
        Realiza una mutación donde cada gen de cada individuo tiene una probabilidad de mutar 
        a la posición de un gen de un individuo seleccionado al azar de los mejores individuos de la población.
        @param poblacion: Una lista de individuos (listas).

        @return: None, es efecto colateral mutando los individuos
                 en la misma lista

        """
        if not individuos:
            return

        mejor_tamano = max(1, len(self.población) // 3)
        mejores = [ind for (_, ind) in sorted(self.población,
                                              key=lambda x: x[0],
                                              reverse=True)[:mejor_tamano]]

        for individuo in individuos:
            for i in range(len(individuo)):
                if random.random() < (self.prob_muta if prob_muta is None else prob_muta):
                    donante = random.choice(mejores)
                    valor = donante[random.randrange(len(donante))]
                    if valor != individuo[i]:
                        j = individuo.index(valor)
                        individuo[i], individuo[j] = individuo[j], individuo[i]

    def reemplazo_generacional(self, individuos):
        """
        Realiza el reemplazo generacional mediante crowding.

        Cada hijo compite con el padre más similar y reemplaza solo si es mejor.

        @param individuos: Una lista de cromosomas de hijos que pueden
                           usarse en el reemplazo
        @return: None (todo lo cambia internamente)

        """
        if not individuos:
            return

        hijos = [(self.adaptación(hijo), hijo) for hijo in individuos]
        padres_disponibles = list(range(len(self.población)))
        poblacion_nueva = list(self.población)

        for aptitud_hijo, hijo in sorted(hijos, reverse=True):
            if not padres_disponibles:
                break
            mejor_idx = None
            mejor_dist = None
            for idx in padres_disponibles:
                dist = self._distancia(hijo, self.población[idx][1])
                if mejor_dist is None or dist < mejor_dist:
                    mejor_dist = dist
                    mejor_idx = idx
            if mejor_idx is None:
                continue
            if aptitud_hijo > self.población[mejor_idx][0]:
                poblacion_nueva[mejor_idx] = (aptitud_hijo, hijo)
            padres_disponibles.remove(mejor_idx)

        self.población = poblacion_nueva


if __name__ == "__main__":
    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1
    g_propio = GeneticoPermutacionesPropio(genetico.ProblemaTonto(10), 10, prob_muta=0.1)
    genetico.prueba(g_propio)