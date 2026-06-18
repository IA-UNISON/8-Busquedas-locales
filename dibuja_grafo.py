#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dibuja_grafo.py
------------

Dibujar un grafo utilizando métodos de optimización

Estos métodos no son los que se utilizan en el dibujo de
gráfos por computadora pero da una idea de la utilidad de los métodos de
optimización en un problema divertido.

Para realizar este problema es necesario contar con el módulo Pillow
instalado (en Anaconda se instala por default. Si no se encuentra instalado,
desde la termnal se puede instalar utilizando

$pip install pillow

"""

__author__ = 'Escribe aquí tu nombre'

import blocales
import random
import itertools
import math
import time
from PIL import Image, ImageDraw


class problema_grafica_grafo(blocales.Problema):

    """
    Clase para el dibujo de un grafo simple no dirigido

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, en forma de
        lista (no conjunto, el orden es importante a la hora de
        graficar), y un conjunto (tambien en forma de lista) de pares
        ordenados de vertices, lo que forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a
        mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con pares de vertices, los cuales
                        definen las aristas.
        @param dimension_imagen: Entero con la dimension de la imagen
                                 en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema de define como:

           s = [s(1), s(2),..., s(2*len(vertices))],

        en donde s(i) pertenece a {10, 11, ..., self.dim - 10} es la posición
        en x del nodo i/2 si i es par, o la posicion en y
        del nodo (i-1)/2 si i es non y(osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de
                 cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in
                     range(2 * len(self.vertices)))

    def vecinos(self, estado):
        """
        Generador de los vecinos de un estado. En este caso, el
        vecino se obtiene cambiando la posición de un vértice en
        forma aleatoria.

        @param estado: Una tupla con el estado.

        @return: Un generador de estados vecinos

        """
        for i in range(len(estado)):
            vecino = list(estado)
            vecino[i] = max(10,
                            min(self.dim - 10,
                                vecino[i] + random.randint(-10, 10)))
            yield tuple(vecino)
    
    def vecino_aleatorio(self, estado, dmax=20):
        """
        Genera un vecino aleatorio moviendo un vértice completo.

        En lugar de modificar solo una coordenada, se selecciona un vértice
        al azar y se modifican sus coordenadas x e y. Esto produce vecinos
        más naturales para el dibujo del grafo.
        """
        vecino = list(estado)

        # Selecciona un vértice al azar
        vertice = random.randint(0, len(self.vertices) - 1)

        # Cada vértice usa dos posiciones: x = 2*i, y = 2*i + 1
        i = 2 * vertice
        j = i + 1

        vecino[i] = max(10,
                        min(self.dim - 10,
                            vecino[i] + random.randint(-dmax, dmax)))

        vecino[j] = max(10,
                        min(self.dim - 10,
                            vecino[j] + random.randint(-dmax, dmax)))

        return tuple(vecino)

    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado
        es la cantidad de veces que dos aristas se cruzan cuando se dibujan.

        Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.

        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes
        # (default solo cuanta el criterio 1)
        K1 = 10.0 #cruce entre aristas
        K2 = 3.0 #separacion entre vertices
        K3 = 4.0 #angulos pequeñas entre aristas
        K4 = 2.0 #criterio propio

        # Genera un diccionario con el estado y la posición
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

        # Como podras ver en los resultados, el costo inicial
        # propuesto no hace figuras particularmente bonitas, y esto es
        # porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el
        # costo el angulo entre dos aristas conectadas al mismo
        # vertice, dandole un mayor costo si el angulo es muy pequeño
        # (positivo o negativo). Igualemtente se puede penalizar el
        # que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en cuatro partes, una es el
        # numero de cruces (ya programada), otra la distancia entre
        # nodos (ya programada) y otro el angulo entre arista de cada
        # nodo (para programar). Por último, un criterio propio
        #
        # Al final, es necesario darle un peso lineal a cada uno de
        # los subcriterios. ¿Que valores de diste a K1, K2 y K3 respectivamente?
        # 
        # Justifica tu criterio
  

    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo
        si se grafica como dice estado_dic

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de
        # aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los
            # vertices de una arista y los valores (x0B,y0B), (x0B,
            # y0B) para los vertices de la otra arista
            (x0A, y0A) = estado_dic[aristaA[0]]
            (xFA, yFA) = estado_dic[aristaA[1]]
            (x0B, y0B) = estado_dic[aristaB[0]]
            (xFB, yFB) = estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar
            # interseccion entre dos lineas cuidando primero de
            # asegurarse que las lineas no son paralelas (para evitar
            # la división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A)
            if den == 0:
                continue

            # Y entonces sacamos el largo del cruce, normalizado por
            # den. Esto significa que en 0 se encuentran en la primer
            # arista y en 1 en la última. Si los puntos de cruce de
            # ambas lineas se encuentran en valores entre 0 y 1,
            # significa que se cruzan
            puntoA = ((xFB - x0B) * (y0A - y0B) -
                      (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) -
                      (yFA - y0A) * (x0A - x0B)) / den
            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización
        proporcional a cada par de vertices que se encuentren menos
        lejos que min_dist. Si la distancia entre vertices es menor a
        min_dist, entonces calcula una penalización proporcional a
        esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.  @param min_dist: Mínima distancia
                           aceptable en pixeles entre dos vértices en
                           el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total

    def angulo_aristas(self, estado_dic):
        """
        Penaliza ángulos pequeños entre aristas que comparten un mismo vértice.

        Si dos aristas salen del mismo vértice con un ángulo menor a 30 grados,
        se agrega una penalización. Esto ayuda a que el dibujo sea más claro,
        evitando aristas casi encimadas.
        """
        total = 0
        angulo_minimo = math.pi / 6  # 30 grados

        for vertice in self.vertices:
            aristas_incidentes = []

            # Busca todas las aristas que tocan al vértice
            for arista in self.aristas:
                if vertice == arista[0]:
                    aristas_incidentes.append(arista[1])
                elif vertice == arista[1]:
                    aristas_incidentes.append(arista[0])

            # Compara cada par de aristas que salen del mismo vértice
            for v1, v2 in itertools.combinations(aristas_incidentes, 2):
                x0, y0 = estado_dic[vertice]
                x1, y1 = estado_dic[v1]
                x2, y2 = estado_dic[v2]

                vector1 = (x1 - x0, y1 - y0)
                vector2 = (x2 - x0, y2 - y0)

                norma1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
                norma2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

                if norma1 == 0 or norma2 == 0:
                    continue

                producto_punto = vector1[0] * vector2[0] + vector1[1] * vector2[1]
                coseno = producto_punto / (norma1 * norma2)

                # Evita errores numéricos fuera del rango [-1, 1]
                coseno = max(-1, min(1, coseno))

                angulo = math.acos(coseno)

                if angulo < angulo_minimo:
                    total += 1.0 - (angulo / angulo_minimo)

        return total

    def criterio_propio(self, estado_dic):
        """
        Criterio propio: penaliza aristas demasiado largas.

        La idea es evitar dibujos muy dispersos, donde algunos vértices quedan
        muy alejados y las aristas cruzan casi toda la imagen. Si una arista mide
        más de una distancia máxima deseada, se agrega una penalización
        proporcional.
        """
        total = 0
        longitud_maxima = self.dim / 2

        for v1, v2 in self.aristas:
            x1, y1 = estado_dic[v1]
            x2, y2 = estado_dic[v2]

            distancia = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            if distancia > longitud_maxima:
                total += (distancia - longitud_maxima) / longitud_maxima

        return total

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma
        de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada
                 arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1])
                for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None, filename="prueba.gif"):
        """
        Dibuja el grafo utilizando el modulo pillow, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es la
        posición en x y y respectivamente de cada vertice. dim es la
        dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        # Imagen en blanco
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))
        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))

        imagen.save(filename)


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    dimension = 400

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para
    # ajustarlo.
    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    costo_inicial = grafo_sencillo.costo(estado_aleatorio)
    grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
    print("Costo del estado aleatorio: {}".format(costo_inicial))

    # Ahora vamos a encontrar donde deben de estar los puntos
    t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("\nUtilizando la calendarización por default")
    print("Costo de la solución encontrada: {}".format(costo_final))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
        # Prueba con calendarización exponencial
    T0 = 50
    alpha = 0.995
    calendarizador_exp = (T0 * (alpha ** i) for i in range(int(1e6)))

    t_inicial = time.time()
    solucion_exp = blocales.temple_simulado(
        grafo_sencillo,
        calendarizador=calendarizador_exp
    )
    t_final = time.time()

    costo_exp = grafo_sencillo.costo(solucion_exp)
    grafo_sencillo.dibuja_grafo(solucion_exp, "prueba_final_exp.gif")

    print("\nUtilizando calendarización exponencial")
    print("Costo de la solución encontrada: {}".format(costo_exp))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
        # ------------------------------------------------------------
    # Grafo más feo inventado para la tarea
    # ------------------------------------------------------------
    vertices_feo = ['A', 'B', 'C', 'D', 'E',
                    'F', 'G', 'H', 'I', 'J']

    aristas_feo = [
        ('A', 'F'), ('A', 'G'), ('A', 'H'),
        ('B', 'G'), ('B', 'I'), ('B', 'E'),
        ('C', 'H'), ('C', 'J'), ('C', 'F'),
        ('D', 'I'), ('D', 'F'),
        ('E', 'J'), ('E', 'G'),
        ('F', 'I'),
        ('G', 'J'),
        ('H', 'I'),
        ('A', 'J'),
        ('D', 'H')
    ]

    grafo_feo = problema_grafica_grafo(vertices_feo,
                                       aristas_feo,
                                       dimension)

    estado_feo_inicial = grafo_feo.estado_aleatorio()
    costo_feo_inicial = grafo_feo.costo(estado_feo_inicial)
    grafo_feo.dibuja_grafo(estado_feo_inicial, "grafo_feo_inicial.gif")

    print("\nGrafo feo inventado")
    print("Costo inicial: {}".format(costo_feo_inicial))

    # Usamos la calendarización exponencial porque fue la que dio mejor resultado
    T0 = 50
    alpha = 0.995
    calendarizador_feo = (T0 * (alpha ** i) for i in range(int(1e6)))

    t_inicial = time.time()
    solucion_feo = blocales.temple_simulado(
        grafo_feo,
        calendarizador=calendarizador_feo
    )
    t_final = time.time()

    costo_feo_final = grafo_feo.costo(solucion_feo)
    grafo_feo.dibuja_grafo(solucion_feo, "grafo_feo_final.gif")

    print("Costo final: {}".format(costo_feo_final))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizar una función de calendarización acorde con
    # el metodo en que se genera el vecino aleatorio.  Existen en la
    # literatura varias combinaciones. Busca en la literatura
    # diferentes métodos de calendarización (al menos uno más
    # diferente al que se encuentra programado) y ajusta los
    # parámetros para que obtenga la mejor solución posible en el
    # menor tiempo posible.
    #
    # Inventate un grafo más feo y muestra como el temple simulado lo hace lucir mejor.
    #
    # Escribe aqui tus conclusiones
    #


if __name__ == '__main__':
    main()
