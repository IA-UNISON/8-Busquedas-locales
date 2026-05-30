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

__author__ = 'Karol Burrola'


class GeneticoPermutacionesPropio(genetico.Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self, problema, n_población, generaciones_a_tolerar=10):
        """
        Aqui puedes poner algunos de los parámetros
        que quieras utilizar en tu clase

        Para esta tarea vamos a cambiar la forma de representación
        para que se puedan utilizar operadores clásicos (esto implica
        reescribir los métodos estáticos cadea_a_estado y
        estado_a_cadena).

        """
        self.generaciones_a_tolerar = generaciones_a_tolerar
        self.contador = 0
        self.mejor = -1.0
        self.nombre = 'Algoritmo CHC (Cataclismos) - Karol Burrola'
        super().__init__(problema, n_población)
        self.umbral_hamming = len(problema.estado_aleatorio()) // 4

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas independiente
        del problema de permutación

        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres

        """
        longitud = len(estado)
        cadena = [0.0] * longitud
        for posicion, valor in enumerate(estado):
            cadena[valor] = float(posicion)
        return cadena

    @staticmethod
    def cadena_a_estado(cadena):
        """
        Convierte una cadena de cromosomas a un estado donde el estado es
        una posible solución a un problema de permutaciones

        @param cadena: Una lista de cromosomas o valores
        @return: Una tupla con un estado válido

        """
        indices = list(range(len(cadena)))
        indices.sort(key=lambda i: cadena[i])
        return tuple(indices)

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
        Seleccion de estados

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        Emparejamiento aleatorio con prevención de incesto:
        Dos padres solo se cruzan si la mitad de sus genes distintos supera el umbral de hamming,
        si no hay parejas válidas, el umbral se reduce en 1 para permitir más cruces en la siguiente
        generación.
        """
        lista_indices = list(range(self.n_población))
        random.shuffle(lista_indices)

        parejas = []
        for i in range(0, self.n_población - 1, 2):
            padre = lista_indices[i]
            madre = lista_indices[i + 1]
            c1 = self.población[padre][1]
            c2 = self.población[madre][1]

            distancia = sum(1 for a, b in zip(c1, c2) if a != b)

            if distancia // 2 > self.umbral_hamming:
                parejas.append((padre, madre))

        if not parejas:
            self.umbral_hamming = max(0, self.umbral_hamming - 1)

        return parejas

    def cruza_individual(self, cadena1, cadena2):
        """
        Intercambia exactamente la mitad de las posiciones donde los padres difieren, elegidas al azar.

        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo

        """
        hijo = cadena1[:]

        posiciones_distintas = [i for i in range(len(cadena1))
                                if cadena1[i] != cadena2[i]]

        n_intercambio = len(posiciones_distintas) // 2
        posiciones_a_intercambiar = random.sample(posiciones_distintas, n_intercambio)

        for i in posiciones_a_intercambiar:
            hijo[i] = cadena2[i]

        return hijo

    def mutación(self, individuos):
        """
        En CHC la mutación no existe, la diversidad se genera únicamente por el cataclismo.

        @param poblacion: Una lista de individuos (listas).

        @return: None, es efecto colateral mutando los individuos
                 en la misma lista

        """
        pass

    def reemplazo_generacional(self, individuos):
        """
        Realiza el reemplazo generacional diferente al elitismo

        @param individuos: Una lista de cromosomas de hijos que pueden
                           usarse en el reemplazo
        @return: None

        Por default usamos solo el elitismo de conservar al mejor, solo si es
        mejor que lo que hemos encontrado hasta el momento.

        Aquí, padres e hijos compiten ya que solo sobreviven los mejores, si la población se estanca
        generaciones seguidas, ocurre un cataclismo: Se conserva al mejor y se repobla el resto
        con individuos aleatorios.

        """
        hijos_evaluados = [(self.adaptación(hijo), hijo) for hijo in individuos]

        poblacion_total = self.población + hijos_evaluados
        poblacion_total.sort(reverse=True)
        self.población = poblacion_total[:self.n_población]

        mejor_actual = self.población[0][0]

        if mejor_actual > self.mejor:
            self.mejor = mejor_actual
            self.contador = 0
        else:
            self.contador += 1

        if self.contador >= self.generaciones_a_tolerar:
            mejor_sobreviviente = self.población[0]
            nueva_poblacion = [mejor_sobreviviente]

            for _ in range(self.n_población - 1):
                estado_azar = self.problema.estado_aleatorio()
                cadena_azar = self.estado_a_cadena(estado_azar)
                b = self.adaptación(cadena_azar)
                nueva_poblacion.append((b, cadena_azar))

            self.población = nueva_poblacion
            self.contador = 0
            self.umbral_hamming = len(self.problema.estado_aleatorio()) // 4

if __name__ == "__main__":
    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1
    g_propio = GeneticoPermutacionesPropio(genetico.ProblemaTonto(10), 10)
    genetico.prueba(g_propio)