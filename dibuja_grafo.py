#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dibuja_grafo.py
------------

Dibujar un grafo utilizando métodos de optimización

"""

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
        return tuple(random.randint(10, self.dim - 10) for _ in
                     range(2 * len(self.vertices)))

    def vecinos(self, estado):
        for i in range(len(estado)):
            vecino = list(estado)
            vecino[i] = max(10,
                            min(self.dim - 10,
                                vecino[i] + random.randint(-10, 10)))
            yield tuple(vecino)
    
    def vecino_aleatorio(self, estado, dmax=10):
        vecino = list(estado)
        vertex_idx = random.randint(0, len(self.vertices) - 1)
        x_idx = 2 * vertex_idx
        y_idx = 2 * vertex_idx + 1
        vecino[x_idx] = max(10, min(self.dim - 10, vecino[x_idx] + random.randint(-dmax, dmax)))
        vecino[y_idx] = max(10, min(self.dim - 10, vecino[y_idx] + random.randint(-dmax, dmax)))
        return tuple(vecino)

    def costo(self, estado):
        K1 = 1.0  # Cruces
        K2 = 0.3  # Proximidad
        K3 = 0.5  # Ángulos
        K4 = 0.2  # Longitud aristas

        estado_dic = self.estado2dic(estado)
        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

    def numero_de_cruces(self, estado_dic):
        total = 0
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):
            (x0A, y0A) = estado_dic[aristaA[0]]
            (xFA, yFA) = estado_dic[aristaA[1]]
            (x0B, y0B) = estado_dic[aristaB[0]]
            (xFB, yFB) = estado_dic[aristaB[1]]
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A)
            if den == 0:
                continue
            puntoA = ((xFB - x0B) * (y0A - y0B) - (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) - (yFA - y0A) * (x0A - x0B)) / den
            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total

    def angulo_aristas(self, estado_dic):
        penalizacion = 0
        min_angulo = math.pi / 6  # 30 grados
        for vertice in self.vertices:
            aristas_conectadas = [arista for arista in self.aristas if vertice in arista]
            if len(aristas_conectadas) < 2:
                continue
            vectores = []
            for arista in aristas_conectadas:
                v_otro = arista[0] if arista[1] == vertice else arista[1]
                dx = estado_dic[v_otro][0] - estado_dic[vertice][0]
                dy = estado_dic[v_otro][1] - estado_dic[vertice][1]
                vectores.append((dx, dy))
            for (v1, v2) in itertools.combinations(vectores, 2):
                producto_punto = v1[0]*v2[0] + v1[1]*v2[1]
                mag_v1 = math.hypot(*v1)
                mag_v2 = math.hypot(*v2)
                if mag_v1 == 0 or mag_v2 == 0:
                    continue
                cos_theta = producto_punto / (mag_v1 * mag_v2)
                cos_theta = max(-1, min(1, cos_theta))
                angulo = math.acos(cos_theta)
                if angulo < min_angulo:
                    penalizacion += (min_angulo - angulo) / min_angulo
        return penalizacion

    def criterio_propio(self, estado_dic):
        penalizacion = 0
        max_longitud = self.dim * 0.4  # 40% del tamaño
        for v1, v2 in self.aristas:
            x1, y1 = estado_dic[v1]
            x2, y2 = estado_dic[v2]
            longitud = math.hypot(x2 - x1, y2 - y1)
            if longitud > max_longitud:
                penalizacion += (longitud - max_longitud) / max_longitud
        return penalizacion

    def estado2dic(self, estado):
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1])
                for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None, filename="prueba.gif"):
        if not estado:
            estado = self.estado_aleatorio()
        lugar = self.estado2dic(estado)
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))
        dibujar = ImageDraw.ImageDraw(imagen)
        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))
        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))
        imagen.save(filename)


def main():
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'), ('E', 'F'), ('H', 'E'), ('D', 'B'),
                        ('H', 'G'), ('A', 'E'), ('C', 'F'), ('H', 'B'),
                        ('F', 'A'), ('C', 'B'), ('H', 'F')]
    dimension = 400

    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    # Calendarización exponencial
    costos = [grafo_sencillo.costo(grafo_sencillo.estado_aleatorio()) for _ in range(10)]
    T_ini = 2 * (max(costos) - min(costos))
    alpha = 0.95
    calendarizador = (T_ini * (alpha ** i) for i in itertools.count())

    t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo, calendarizador)
    t_final = time.time()

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("Costo final:", grafo_sencillo.costo(solucion))
    print("Tiempo:", t_final - t_inicial)


if __name__ == '__main__':
    main()