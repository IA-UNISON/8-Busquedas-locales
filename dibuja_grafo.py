#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dibuja_grafo.py
------------

Dibujar un grafo utilizando métodos de optimización
"""

__author__ = 'Rosario Luna Ortiz'

import blocales
import random
import itertools
import math
import time
from PIL import Image, ImageDraw


class problema_grafica_grafo(blocales.Problema):

    def __init__(self, vertices, aristas, dimension_imagen=400):

        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):

        return tuple(
            random.randint(10, self.dim - 10)
            for _ in range(2 * len(self.vertices))
        )

    def vecinos(self, estado):

        for i in range(len(estado)):

            vecino = list(estado)

            vecino[i] = max(
                10,
                min(
                    self.dim - 10,
                    vecino[i] + random.randint(-10, 10)
                )
            )

            yield tuple(vecino)

    def vecino_aleatorio(self, estado, dmax=30):

        vecino = list(estado)

        v = random.randint(0, len(self.vertices) - 1)

        i = 2 * v
        j = i + 1

        vecino[i] = max(
            10,
            min(
                self.dim - 10,
                vecino[i] + random.randint(-dmax, dmax)
            )
        )

        vecino[j] = max(
            10,
            min(
                self.dim - 10,
                vecino[j] + random.randint(-dmax, dmax)
            )
        )

        return tuple(vecino)

    def costo(self, estado):

        K1 = 10.0
        K2 = 4.0
        K3 = 2.0
        K4 = 1.0

        estado_dic = self.estado2dic(estado)

        return (
            K1 * self.numero_de_cruces(estado_dic) +
            K2 * self.separacion_vertices(estado_dic) +
            K3 * self.angulo_aristas(estado_dic) +
            K4 * self.criterio_propio(estado_dic)
        )

    def numero_de_cruces(self, estado_dic):

        total = 0

        for (aristaA, aristaB) in itertools.combinations(
                self.aristas, 2):

            (x0A, y0A) = estado_dic[aristaA[0]]
            (xFA, yFA) = estado_dic[aristaA[1]]

            (x0B, y0B) = estado_dic[aristaB[0]]
            (xFB, yFB) = estado_dic[aristaB[1]]

            den = (
                (xFA - x0A) * (yFB - y0B) -
                (xFB - x0B) * (yFA - y0A)
            )

            if den == 0:
                continue

            puntoA = (
                (xFB - x0B) * (y0A - y0B) -
                (yFB - y0B) * (x0A - x0B)
            ) / den

            puntoB = (
                (xFA - x0A) * (y0A - y0B) -
                (yFA - y0A) * (x0A - x0B)
            ) / den

            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1

        return total

    def separacion_vertices(self,
                             estado_dic,
                             min_dist=50):

        total = 0

        for (v1, v2) in itertools.combinations(
                self.vertices, 2):

            (x1, y1) = estado_dic[v1]
            (x2, y2) = estado_dic[v2]

            dist = math.sqrt(
                (x1 - x2) ** 2 +
                (y1 - y2) ** 2
            )

            if dist < min_dist:

                total += (
                    1.0 - (dist / min_dist)
                )

        return total

    def angulo_aristas(self, estado_dic):

        total = 0

        angulo_minimo = math.pi / 6

        for vertice in self.vertices:

            conexiones = []

            for (a, b) in self.aristas:

                if a == vertice:
                    conexiones.append(b)

                elif b == vertice:
                    conexiones.append(a)

            for v1, v2 in itertools.combinations(
                    conexiones, 2):

                x0, y0 = estado_dic[vertice]

                x1, y1 = estado_dic[v1]
                x2, y2 = estado_dic[v2]

                ax = x1 - x0
                ay = y1 - y0

                bx = x2 - x0
                by = y2 - y0

                prod = ax * bx + ay * by

                mag_a = math.sqrt(ax ** 2 + ay ** 2)
                mag_b = math.sqrt(bx ** 2 + by ** 2)

                if mag_a == 0 or mag_b == 0:
                    continue

                coseno = prod / (mag_a * mag_b)

                coseno = max(-1, min(1, coseno))

                angulo = math.acos(coseno)

                if angulo < angulo_minimo:

                    total += (
                        angulo_minimo - angulo
                    )

        return total

    def criterio_propio(self, estado_dic):

        total = 0

        margen = 30

        for v in self.vertices:

            x, y = estado_dic[v]

            if x < margen:
                total += (margen - x)

            if y < margen:
                total += (margen - y)

            if x > self.dim - margen:
                total += (
                    x - (self.dim - margen)
                )

            if y > self.dim - margen:
                total += (
                    y - (self.dim - margen)
                )

        return total

    def estado2dic(self, estado):

        return {
            self.vertices[i]:
            (estado[2 * i], estado[2 * i + 1])

            for i in range(len(self.vertices))
        }

    def dibuja_grafo(self,
                     estado=None,
                     filename="prueba.gif"):

        if not estado:
            estado = self.estado_aleatorio()

        lugar = self.estado2dic(estado)

        imagen = Image.new(
            'RGB',
            (self.dim, self.dim),
            (255, 255, 255)
        )

        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:

            dibujar.line(
                (lugar[v1], lugar[v2]),
                fill=(255, 0, 0)
            )

        for v in self.vertices:

            dibujar.text(
                lugar[v],
                v,
                (0, 0, 0)
            )

        imagen.save(filename)


def main():

    vertices_sencillo = [
        'A', 'B', 'C', 'D', 'E',
        'F', 'G', 'H', 'I', 'J'
    ]

    aristas_sencillo = [
        ('A', 'B'),
        ('A', 'C'),
        ('A', 'D'),
        ('B', 'E'),
        ('C', 'F'),
        ('D', 'G'),
        ('E', 'H'),
        ('F', 'I'),
        ('G', 'J'),
        ('H', 'I'),
        ('I', 'J'),
        ('B', 'J'),
        ('C', 'H'),
        ('D', 'I'),
        ('E', 'G')
    ]

    dimension = 400

    grafo_sencillo = problema_grafica_grafo(
        vertices_sencillo,
        aristas_sencillo,
        dimension
    )

    estado_aleatorio = \
        grafo_sencillo.estado_aleatorio()

    costo_inicial = \
        grafo_sencillo.costo(estado_aleatorio)

    grafo_sencillo.dibuja_grafo(
        estado_aleatorio,
        "prueba_inicial.gif"
    )

    print("Costo inicial:", costo_inicial)

    calendarizador = (
        1000 * (0.95 ** i)
        for i in range(10000)
    )

    t_inicial = time.time()

    solucion = blocales.temple_simulado(
        grafo_sencillo,
        calendarizador
    )

    t_final = time.time()

    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(
        solucion,
        "prueba_final.gif"
    )

    print("\nTemple Simulado")
    print("Costo final:", costo_final)
    print("Tiempo:", t_final - t_inicial)


if __name__ == '__main__':
    main()