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

__author__ = 'Alejandro Barreras Gutiérrez'

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
    
    def vecino_aleatorio(self, estado, dmax=40):
        """
        Encuentra un vecino en forma aleatoria. En estea primera
        versión lo que hacemos es tomar un valor aleatorio, y
        sumarle o restarle x pixeles al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar
        como hacer un mejor vecino aleatorio y comparar las ventajas de
        hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.
        @param dispersion: Un flotante con el valor de dispersión para el
                           vertice seleccionado

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        #vecino = list(estado)
        #i = random.randint(0, len(vecino) - 1)
        #vecino[i] = max(10,
        #                min(self.dim - 10,
        #                    vecino[i] + random.randint(-dmax,  dmax)))
        #return tuple(vecino)
        #
        # Por supuesto que esta no es la mejor manera de generar vecinos.
        #
        # Propon una manera alternativa de vecino_aleatorio y muestra que
        # con tu propuesta se obtienen resultados mejores o en menor tiempo

        vecino = list(estado)
        indice_vertice = random.randint(0, len(self.vertices) - 1)
        ix = indice_vertice * 2
        iy = indice_vertice * 2 + 1

        nuevo_x = vecino[ix] + random.randint(-dmax, dmax)
        nuevo_y = vecino[iy] + random.randint(-dmax, dmax)

        vecino[ix] = max(10, min(self.dim - 10, nuevo_x))
        vecino[iy] = max(10, min(self.dim - 10, nuevo_y))

        return tuple(vecino)
    
        # En la primera version es probable que solo se modificaba una coordenada a la vez.
        # En esta propuesta, se identifican las coordenadas (x, y) de un vertice y despues se modifican ambos al mismo tiempo
        # asi agregando un valor aleatorio entre -dmax y dmax.
        #
        # Gracias a esto se generan mejores resultados porque el algoritmo puede explorar de forma diagonal y no se estanca 
        # con puros movimientos verticales, o mas bien evita caer en esos problemas.

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
        K1 = 10.0
        K2 = 6.0
        K3 = 3.0
        K4 = 1.0

        # Genera un diccionario con el estado y la posición
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
        # 
        # Justifica tu criterio
        #
        # - K1 = 10.0 Es el mas importante ya que un cruce hace que el grafo sea confuso.
        # - K2 = 6.0 Tambien es importante la separacion ya que nodos encima de otros lo hace ilegible.
        # - K3 = 3.0 Mejora lo estetico del grafo.
        # - K4 = 1.0 Tiene poco peso ya que es cosmetico.

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
        A partir de una posicion "estado", devuelve una penalizacion
        proporcional a cada angulo entre aristas menor a pi/6 rad (30
        grados). Los angulos de pi/6 o mayores no llevan ninguna
        penalización, y la penalizacion crece conforme el angulo es
        menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        # Agrega el método que considere el angulo entre aristas de
        # cada vertice. Dale diferente peso a cada criterio hasta

        angulo_critico = math.pi / 6
        total = 0

        for v in self.vertices:
            aristas_v = [arista for arista in self.aristas if v in arista]
            n = len(aristas_v)
            
            for i in range(n):
                for j in range(i + 1, n):
                    aristaA = aristas_v[i]
                    aristaB = aristas_v[j]

                    otro_A = aristaA[1] if aristaA[0] == v else aristaA[0]
                    otro_B = aristaB[1] if aristaB[0] == v else aristaB[0]

                    x_v, y_v = estado_dic[v]
                    v1x, v1y = estado_dic[otro_A][0] - x_v, estado_dic[otro_A][1] - y_v
                    v2x, v2y = estado_dic[otro_B][0] - x_v, estado_dic[otro_B][1] - y_v

                    magnitud1 = math.sqrt(v1x**2 + v1y**2)
                    magnitud2 = math.sqrt(v2x**2 + v2y**2)
                    if magnitud1 == 0 or magnitud2 == 0:
                        continue

                    producto_punto = v1x * v2x + v1y * v2y

                    cos_theta = producto_punto / (magnitud1 * magnitud2)

                    cos_theta = max(-1.0, min(1.0, cos_theta))
                    theta = math.acos(cos_theta)
                    if theta < angulo_critico:
                        penalizacion = (angulo_critico - theta) / angulo_critico
                        total += penalizacion
        return total

    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea
        conveniente para que un grafo luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        # Desarrolla un criterio propio y ajusta su importancia en el
        # costo total con K4 
        # ¿Mejora el resultado?
        # 
        # Si, se nota bastante la diferencia.
        #  
        # ¿En que mejora el resultado final?
        # Evita que ciertas lineas parezcan estar conectadas cuando en realidad no lo estan. 
        
        total = 0.0
        min_distancia = 15.0

        for v in self.vertices:
            xp, yp = estado_dic[v]
            for (v1, v2) in self.aristas:
                if v == v1 or v == v2:
                    continue

                x1, y1 = estado_dic[v1]
                x2, y2 = estado_dic[v2]

                dx, dy = x2 - x1, y2 - y1
                segmento_largo = math.sqrt(dx**2 + dy**2)
                if segmento_largo == 0:
                    continue

                t = max(0, min(1, ((xp-x1)*dx + (yp-y1)*dy) / (segmento_largo**2)))
                distancia = math.sqrt((xp - (x1 + t*dx))**2 + (yp - (y1 + t*dy))**2)

                if distancia < min_distancia:
                    total += (1.0 - distancia / min_distancia)

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
    solucion_default = blocales.temple_simulado(grafo_sencillo)
    costo_final = grafo_sencillo.costo(solucion_default)
    t_final = time.time()

    grafo_sencillo.dibuja_grafo(solucion_default, "prueba_final.gif")
    print("\nUtilizando la calendarización por default")
    print("Costo de la solución encontrada: {}".format(costo_final))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))


    # --------------------


    T_ini = 1000.0
    alpha = 0.995
    iteraciones = 100000
    calendarizador_geo = (T_ini * (alpha ** i) for i in range(iteraciones))

    t_inicial = time.time()
    solucion_geo = blocales.temple_simulado(grafo_sencillo, calendarizador = calendarizador_geo)
    t_final = time.time()

    grafo_sencillo.dibuja_grafo(solucion_geo, "prueba_final_geometrica.gif")
    print("\nCalendarizacion geometrica")
    print("Costo encontrado: {}".format(grafo_sencillo.costo(solucion_geo)))
    print("Tiempo: {:.2f} segundos".format(t_final - t_inicial))

    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    #
    # Un T_ini alto combinado con un alpha lento y alrededor de 100,000 iteraciones.
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    # El criterio (K1) es el mas importante ya que es el de numero de cruces, entonces si no tiene mucho peso, el algoritmo
    # empieza a amontonar los nodos o las lineas haciendolo dificil de comprender. Ademas, se puede observar que en la calendarizacion
    # geometrica tiende a dar mejores resultados que la default gracias a su enfriamento mas controlado.
    #
    # Inventate un grafo más feo y muestra como el temple simulado lo hace lucir mejor.

    vertices_feo = ['1', '2', '3', '4', '5']
    aristas_feo = []

    n = len(vertices_feo)
    for i in range(n):
        for j in range(i + 1, n):
            aristas_feo.append((vertices_feo[i], vertices_feo[j]))
    
    grafo_feo = problema_grafica_grafo(vertices_feo, aristas_feo, dimension)
    estado_feo_inicial = grafo_feo.estado_aleatorio()
    grafo_feo.dibuja_grafo(estado_feo_inicial, "grafo_feo_inicial.gif")
    
    print("\nGrafo feo")
    print("Costo inicial: {}".format(grafo_feo.costo(estado_feo_inicial)))

    T_ini_feo = 1000.0
    alpha_feo = 0.995
    iteraciones_feo = 100000
    calendarizador_feo = (T_ini_feo * (alpha_feo ** i) for i in range(iteraciones_feo))

    t_inicial = time.time()
    solucion_feo = blocales.temple_simulado(grafo_feo, calendarizador=calendarizador_feo)
    t_final = time.time()

    grafo_feo.dibuja_grafo(solucion_feo, "grafo_feo_final.gif")
    print("Costo final: {}".format(grafo_feo.costo(solucion_feo)))
    print("Tiempo: {:.2f} segundos".format(t_final - t_inicial))

    # Escribe aqui tus conclusiones
    #
    # El temple simulado es muy eficiente para ordenar grafos, pero influye mucho como estan ajustados los parametros. Es
    # muy importante encontrar un equilibrio con los pesos en la funcion de costo. Y como ultimo, el grafo feo muestra que 
    # cuando no hay una solucion perfecta el algoritmo busca la estructura mas simetrica que se puede.


if __name__ == '__main__':
    main()
