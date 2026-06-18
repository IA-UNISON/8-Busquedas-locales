#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genetico_tarea.py
-----------------

En este módulo vas a desarrollar tu propio algoritmo
genético para resolver problemas de permutaciones.

La propuesta implementada usa:
- selección por torneo,
- cruza OX,
- mutación por intercambio,
- reemplazo generacional con mezcla de padres e hijos.
"""

import random
import genetico

__author__ = 'Joaquin Sotelo'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones.

    Esta versión es diferente a GeneticoPermutaciones de genetico.py porque
    no usa selección por ruleta ni la misma cruza. En su lugar utiliza torneo,
    cruza OX y reemplazo generacional por supervivencia de los más aptos.
    """

    def __init__(self, problema, n_población, prob_muta=0.1,
                 tamaño_torneo=3):
        """
        Inicializa el algoritmo genético propio.

        @param problema: Problema de permutaciones.
        @param n_población: Tamaño de la población.
        @param prob_muta: Probabilidad de mutación de cada individuo.
        @param tamaño_torneo: Número de individuos que compiten en torneo.
        """
        self.prob_muta = prob_muta
        self.tamaño_torneo = tamaño_torneo
        self.nombre = ('propuesto por Joaquin Sotelo con selección por torneo, '
                       'cruza OX y prob. de mutación ' + str(prob_muta))
        super().__init__(problema, n_población)

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas independiente
        del problema de permutación.

        @param estado: Una tupla con un estado.
        @return: Una lista con una cadena de cromosomas.
        """
        return list(estado)

    @staticmethod
    def cadena_a_estado(cadena):
        """
        Convierte una cadena de cromosomas a un estado válido.

        @param cadena: Una lista de cromosomas o valores.
        @return: Una tupla con un estado válido.
        """
        return tuple(cadena)

    def adaptación(self, individuo):
        """
        Calcula la adaptación de un individuo.

        Mientras menor sea el costo del problema, mayor será la adaptación.
        Se usa 1 / (1 + costo) para evitar división entre cero.

        @param individuo: Una lista de cromosomas.
        @return: Un número con la adaptación del individuo.
        """
        estado = self.cadena_a_estado(individuo)
        costo = self.problema.costo(estado)
        return 1 / (1.0 + costo)

    def selección(self):
        """
        Selección de estados mediante torneo.

        @return: Una lista con pares de índices de los individuos que se van
                 a cruzar.
        """
        def torneo():
            tamaño = min(self.tamaño_torneo, self.n_población)
            indices = random.sample(range(self.n_población), tamaño)
            return max(indices, key=lambda i: self.población[i][0])

        parejas = []
        for _ in range(self.n_población):
            padre1 = torneo()
            padre2 = torneo()
            while padre2 == padre1 and self.n_población > 1:
                padre2 = torneo()
            parejas.append((padre1, padre2))

        return parejas

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza OX, también conocida como Order Crossover.

        Copia un segmento del primer padre y completa el resto con los genes
        del segundo padre en el orden en que aparecen, evitando repetidos.

        @param cadena1: Una lista con un individuo.
        @param cadena2: Una lista con otro individuo.
        @return: Un individuo hijo válido como permutación.
        """
        n = len(cadena1)
        inicio, fin = sorted(random.sample(range(n), 2))

        hijo = [None] * n
        hijo[inicio:fin + 1] = cadena1[inicio:fin + 1]

        posicion = (fin + 1) % n
        genes_padre2 = cadena2[fin + 1:] + cadena2[:fin + 1]

        for gen in genes_padre2:
            if gen not in hijo:
                hijo[posicion] = gen
                posicion = (posicion + 1) % n

        return hijo

    def mutación(self, individuos):
        """
        Mutación por intercambio.

        Con probabilidad self.prob_muta, intercambia dos posiciones del
        individuo. Esto mantiene siempre una permutación válida.

        @param individuos: Una lista de individuos.
        @return: None. Modifica la lista por efecto colateral.
        """
        for individuo in individuos:
            if random.random() < self.prob_muta:
                i, j = random.sample(range(len(individuo)), 2)
                individuo[i], individuo[j] = individuo[j], individuo[i]

    def reemplazo_generacional(self, individuos):
        """
        Reemplazo generacional por supervivencia de los más aptos.

        Junta la población actual con los hijos y conserva los mejores
        self.n_población individuos.

        @param individuos: Lista de cromosomas hijos.
        @return: None. Actualiza internamente self.población.
        """
        hijos_con_aptitud = [(self.adaptación(individuo), individuo)
                             for individuo in individuos]

        candidatos = self.población + hijos_con_aptitud
        candidatos.sort(reverse=True)
        self.población = candidatos[:self.n_población]


if __name__ == "__main__":
    from nreinas import ProblemaNreinas

    import time

    tamaños = [8, 16, 32, 64, 128]

    for n in tamaños:

        print("\n" + "=" * 40)

        print(f"Probando genético propio con {n} reinas")

        print("=" * 40)

        inicio = time.time()

        g_propio = GeneticoPermutacionesPropio(

            ProblemaNreinas(n),

            n_población=100,

            prob_muta=0.1

        )

        solución = g_propio.busqueda(n_generaciones=500)

        costo = ProblemaNreinas(n).costo(solución)

        fin = time.time()

        print("Solución:", solución)

        print("Costo:", costo)

        print("Tiempo:", fin - inicio)