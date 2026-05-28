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

        en donde s(i) \in {10, 11, ..., self.dim - 10} es la posición
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
    
    def vecino_aleatorio(self, estado, dmax=10):
        """
        encuentra un vecino en forma aleatoria. selecciona un vertice y cambia
        su posicion en x y y de forma simultanea.

        @param estado: Una tupla con el estado.
        @param dmax: dispersion maxima en pixeles

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        vecino = list(estado)
        num_vertices = len(self.vertices)
        k = random.randint(0, num_vertices - 1)
        idx_x = 2 * k
        idx_y = 2 * k + 1
        vecino[idx_x] = max(10, min(self.dim - 10, vecino[idx_x] + random.randint(-dmax, dmax)))
        vecino[idx_y] = max(10, min(self.dim - 10, vecino[idx_y] + random.randint(-dmax, dmax)))
        return tuple(vecino)


    def costo(self, estado):
        """
        calcula el costo total combinando diferentes criterios lineales.
        usamos K1=5.0 para cruces porque es el mas importante, K2=2.0 para la
        separacion de vertices, K3=2.0 para penalizar angulos muy cerrados y
        K4=1.0 para mantener longitudes de aristas uniformes.

        @param estado: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """
        K1 = 5.0
        K2 = 2.0
        K3 = 2.0
        K4 = 1.0

        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

  

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
        devuelve una penalizacion si el angulo entre aristas de un mismo vertice
        es menor a 30 grados (pi / 6 rad).

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        total = 0.0
        for v in self.vertices:
            # encuentra los vecinos conectados a v
            vecinos_v = []
            for (v1, v2) in self.aristas:
                if v1 == v:
                    vecinos_v.append(v2)
                elif v2 == v:
                    vecinos_v.append(v1)
            
            if len(vecinos_v) < 2:
                continue
                
            (x_v, y_v) = estado_dic[v]
            for (u1, u2) in itertools.combinations(vecinos_v, 2):
                (x_1, y_1) = estado_dic[u1]
                (x_2, y_2) = estado_dic[u2]
                
                # calcula vectores y magnitudes
                dx1, dy1 = x_1 - x_v, y_1 - y_v
                dx2, dy2 = x_2 - x_v, y_2 - y_v
                norm_a = math.sqrt(dx1**2 + dy1**2)
                norm_b = math.sqrt(dx2**2 + dy2**2)
                
                if norm_a == 0 or norm_b == 0:
                    total += 1.0
                    continue
                
                # calcula el angulo usando producto punto
                cos_theta = (dx1 * dx2 + dy1 * dy2) / (norm_a * norm_b)
                cos_theta = max(-1.0, min(1.0, cos_theta))
                theta = math.acos(cos_theta)
                
                limite = math.pi / 6
                if theta < limite:
                    total += (1.0 - (theta / limite))
        return total


    def criterio_propio(self, estado_dic):
        """
        penaliza la varianza de la longitud de las aristas para
        buscar que todas tengan una longitud similar (80 pixeles).

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        total = 0.0
        l_ideal = 80.0
        for (v1, v2) in self.aristas:
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            total += ((dist - l_ideal) / l_ideal) ** 2
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


def calendarizador_geometrico(problema, alpha=0.995, tol=0.001):
    """
    calendarizador geometrico que reduce la temperatura multiplicandola
    por un factor constante alpha en cada iteracion.
    """
    costos = [
        problema.costo(problema.estado_aleatorio())
        for _ in range(10 * len(problema.estado_aleatorio()))
    ]
    minimo, maximo = min(costos), max(costos)
    t = 2.0 * (maximo - minimo)
    if t == 0:
        t = 100.0
    while t > tol:
        yield t
        t *= alpha


def calendarizador_lundy_mees(problema, beta=0.001, tol=0.001):
    """
    calendarizador de Lundy-Mees: T = T / (1 + beta * T).
    Es un descenso de temperatura muy suave y continuo.
    """
    costos = [
        problema.costo(problema.estado_aleatorio())
        for _ in range(10 * len(problema.estado_aleatorio()))
    ]
    minimo, maximo = min(costos), max(costos)
    t = 2.0 * (maximo - minimo)
    if t == 0:
        t = 100.0
    while t > tol:
        yield t
        t = t / (1.0 + beta * t)



def main():
    """
    ejecuta las pruebas para el dibujo de grafos con temple simulado.
    """
    # grafo sencillo original
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

    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    costo_inicial = grafo_sencillo.costo(estado_aleatorio)
    grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
    print("Grafo Sencillo:")
    print("Costo del estado aleatorio: {}".format(costo_inicial))

    # prueba con calendarizacion geometrica y vecino mejorado
    t_inicial = time.time()
    cal = calendarizador_geometrico(grafo_sencillo, alpha=0.995)
    solucion = blocales.temple_simulado(grafo_sencillo, cal)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("Utilizando la calendarizacion geometrica:")
    print("  Costo de la solucion encontrada: {}".format(costo_final))
    print("  Tiempo de ejecucion en segundos: {}".format(t_final - t_inicial))

    # prueba con calendarizacion Lundy-Mees y vecino mejorado
    t_inicial = time.time()
    cal = calendarizador_lundy_mees(grafo_sencillo, beta=0.05)
    solucion = blocales.temple_simulado(grafo_sencillo, cal)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final_lundy.gif")
    print("Utilizando la calendarizacion Lundy-Mees:")
    print("  Costo de la solucion encontrada: {}".format(costo_final))
    print("  Tiempo de ejecucion en segundos: {}".format(t_final - t_inicial))

    # grafo mas feo (grafo de petersen)
    print("\nGrafo de Petersen (grafo mas complejo):")
    vertices_petersen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    aristas_petersen = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A'),
        ('F', 'H'), ('H', 'J'), ('J', 'G'), ('G', 'I'), ('I', 'F'),
        ('A', 'F'), ('B', 'G'), ('C', 'H'), ('D', 'I'), ('E', 'J')
    ]
    grafo_petersen = problema_grafica_grafo(vertices_petersen,
                                            aristas_petersen,
                                            dimension)

    est_aleat_petersen = grafo_petersen.estado_aleatorio()
    costo_ini_petersen = grafo_petersen.costo(est_aleat_petersen)
    grafo_petersen.dibuja_grafo(est_aleat_petersen, "petersen_inicial.gif")
    print("Costo inicial: {}".format(costo_ini_petersen))

    t_ini_p = time.time()
    cal_p = calendarizador_geometrico(grafo_petersen, alpha=0.997)
    sol_petersen = blocales.temple_simulado(grafo_petersen, cal_p)
    t_fin_p = time.time()
    costo_fin_petersen = grafo_petersen.costo(sol_petersen)

    grafo_petersen.dibuja_grafo(sol_petersen, "petersen_final.gif")
    print("Utilizando la calendarizacion geometrica:")
    print("  Costo final obtenido: {}".format(costo_fin_petersen))
    print("  Tiempo de ejecucion en segundos: {}".format(t_fin_p - t_ini_p))

    t_ini_p = time.time()
    cal_p = calendarizador_lundy_mees(grafo_petersen, beta=0.015)
    sol_petersen = blocales.temple_simulado(grafo_petersen, cal_p)
    t_fin_p = time.time()
    costo_fin_petersen = grafo_petersen.costo(sol_petersen)

    grafo_petersen.dibuja_grafo(sol_petersen, "petersen_final_lundy.gif")
    print("Utilizando la calendarizacion Lundy-Mees:")
    print("  Costo final obtenido: {}".format(costo_fin_petersen))
    print("  Tiempo de ejecucion en segundos: {}".format(t_fin_p - t_ini_p))



if __name__ == '__main__':
    main()

