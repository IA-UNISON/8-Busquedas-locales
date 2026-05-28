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

__author__ = 'Francisco Ricardo Hernandez Astorga'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self, problema, n_población, prob_muta=0.05):
        """
        Aqui puedes poner algunos de los parámetros
        que quieras utilizar en tu clase

        Para esta tarea vamos a cambiar la forma de representación
        para que se puedan utilizar operadores clásicos (esto implica
        reescribir los métodos estáticos cadea_a_estado y
        estado_a_cadena).

        """
        self.nombre = 'propuesto por el alumno (Lehmer code)'
        self.prob_muta = prob_muta
        super().__init__(problema, n_población)

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas independiente
        del problema de permutación

        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres

        """
        n = len(estado)
        sorted_vals = sorted(estado)
        rank_map = {val: idx for idx, val in enumerate(sorted_vals)}
        ranks = [rank_map[x] for x in estado]
        
        L = list(range(n))
        cadena = []
        for val in ranks:
            idx = L.index(val)
            cadena.append(idx)
            L.pop(idx)
        return cadena

    @staticmethod
    def cadena_a_estado(cadena):
        """
        Convierte una cadena de cromosomas a un estado donde el estado es
        una posible solución a un problema de permutaciones

        @param cadena: Una lista de cromosomas o valores
        @return: Una tupla con un estado válido

        """
        n = len(cadena)
        L = list(range(n))
        estado = []
        for idx in cadena:
            idx = max(0, min(len(L) - 1, int(idx)))
            estado.append(L.pop(idx))
        return tuple(estado)


        
    def adaptación(self, individuo):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado
        mejor, mayor costo, menor adaptción.

        @param individuo: Una lista de cromosomas
        @return un número con la adaptación del individuo

        """
        # La adaptación es inversamente proporcional al costo.
        # Sumamos 1.0 para evitar división entre cero en caso de costo 0.
        return 1.0 / (1.0 + self.problema.costo(self.cadena_a_estado(individuo)))

    def selección(self):
        """
        Seleccion de estados mediante método diferente a la ruleta.
        Utiliza Selección por Torneo (k = 3) para evitar problemas de
        presión selectiva asociados con la ruleta estándar.

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """
        parejas = []
        k_torneo = 3
        for _ in range(self.n_población):
            # Seleccionar padre 1
            idx_padres = random.sample(range(self.n_población), k_torneo)
            padre1 = max(idx_padres, key=lambda idx: self.población[idx][0])
            
            # Seleccionar padre 2
            idx_madres = random.sample(range(self.n_población), k_torneo)
            padre2 = max(idx_madres, key=lambda idx: self.población[idx][0])
            
            parejas.append((padre1, padre2))
        return parejas

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza de un punto (Single-point crossover) sobre el código de Lehmer.
        Dado que ambos padres representan códigos de Lehmer válidos, cualquier
        corte y combinación generará un código de Lehmer válido.

        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo

        """
        n = len(cadena1)
        corte = random.randint(1, n - 1)
        hijo = cadena1[:corte] + cadena2[corte:]
        return hijo

    def mutación(self, individuos):
        """
        Mutación sobre el código de Lehmer.
        Para cada gen i (con rango válido [0, n - 1 - i]), hay una probabilidad
        self.prob_muta de que sea cambiado por un nuevo valor aleatorio en su rango.

        @param individuos: Una lista de individuos (listas).

        @return: None, es efecto colateral mutando los individuos
                 en la misma lista

        """
        for individuo in individuos:
            n = len(individuo)
            for i in range(n):
                if random.random() < self.prob_muta:
                    individuo[i] = random.randint(0, n - 1 - i)

    def reemplazo_generacional(self, individuos):
        """
        Realiza el reemplazo generacional diferente al elitismo simple.
        Mantenemos el 10% de los mejores padres de la población anterior (elite),
        y completamos el resto con los mejores hijos generados.

        @param individuos: Una lista de cromosomas de hijos que pueden
                           usarse en el reemplazo
        @return: None (todo lo cambia internamente)

        """
        # Calcular adaptación de los hijos
        hijos = [(self.adaptación(h), h) for h in individuos]
        
        # Ordenar padres y seleccionar elite (10%)
        self.población.sort(reverse=True)
        n_elite = max(1, self.n_población // 10)
        elites = self.población[:n_elite]
        
        # Combinar elites con hijos y seleccionar los mejores para mantener el tamaño
        combinados = elites + hijos
        combinados.sort(reverse=True)
        
        self.población = combinados[:self.n_población]



if __name__ == "__main__":
    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1
    g_propio = GeneticoPermutacionesPropio(genetico.ProblemaTonto(10), 10)
    genetico.prueba(g_propio)