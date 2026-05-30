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

__author__ = 'Daniel Eduardo Alvarez Terrazas'

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
    
    #def vecino_aleatorio(self, estado, dmax=10):
    #    """
    #    Encuentra un vecino en forma aleatoria. En estea primera
    #    versión lo que hacemos es tomar un valor aleatorio, y
    #    sumarle o restarle x pixeles al azar.

    #    Este es un vecino aleatorio muy malo. Por lo que deberás buscar
    #    como hacer un mejor vecino aleatorio y comparar las ventajas de
    #    hacer un mejor vecino en el algoritmo de temple simulado.

    #    @param estado: Una tupla con el estado.
    #    @param dispersion: Un flotante con el valor de dispersión para el
    #                       vertice seleccionado

    #    @return: Una tupla con un estado vecino al estado de entrada.

    #   """
    #    vecino = list(estado)
    #    i = random.randint(0, len(vecino) - 1)
    #    vecino[i] = max(10,
    #                    min(self.dim - 10,
    #                        vecino[i] + random.randint(-dmax,  dmax)))
    #    return tuple(vecino)

        
        # Por supuesto que esta no es la mejor manera de generar vecinos.
        #
        # Propon una manera alternativa de vecino_aleatorio y muestra que
        # con tu propuesta se obtienen resultados mejores o en menor tiempo

    def vecino_aleatorio(self, estado, dmax=25):

        vecino = list(estado)

        v = random.randint(0, len(self.vertices) - 1)

        ix = 2 * v
        iy = 2 * v + 1

        dx = 0
        dy = 0

        while dx == 0 and dy == 0:
            dx = int(random.gauss(0, dmax / 2))
            dy = int(random.gauss(0, dmax / 2))

        vecino[ix] += dx
        vecino[iy] += dy

        vecino[ix] = max(10, min(self.dim - 10, vecino[ix]))
        vecino[iy] = max(10, min(self.dim - 10, vecino[iy]))

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
        K1 = 5.0   # cruces
        K2 = 1.0    # separacion entre vertices
        K3 = 0.5    # angulos
        K4 = 0.05   # longitud de aristas

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
        # se asignó el mayor peso al número de cruces (K1),
        # ya que es el criterio que más afecta la claridad
        # visual del grafo.
        #
        # la separación entre vértices (K2) ayuda a evitar que
        # los nodos queden demasiado juntos y dificulte la lectura.
        #
        # el criterio de ángulos (K3) penaliza ángulos muy pequeños
        # entre aristas conectadas al mismo vértice, porque generan
        # dibujos más confusos.
        #
        # finalmente, el criterio propio (K4) penaliza aristas muy
        # largas para evitar distribuciones demasiado dispersas,
        # aunque con un peso pequeño para no afectar demasiado
        # la estructura general del grafo.
  

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

        total = 0

        for v in self.vertices:

            # vecinos conectados al vertice v
            conectados = []

            for (a, b) in self.aristas:
                if a == v:
                    conectados.append(b)
                elif b == v:
                    conectados.append(a)

            # comparar pares de aristas
            for n1, n2 in itertools.combinations(conectados, 2):

                x0, y0 = estado_dic[v]
                x1, y1 = estado_dic[n1]
                x2, y2 = estado_dic[n2]

                # vectores
                vx1, vy1 = x1 - x0, y1 - y0
                vx2, vy2 = x2 - x0, y2 - y0

                # producto punto
                prod = vx1 * vx2 + vy1 * vy2

                # magnitudes
                mag1 = math.sqrt(vx1**2 + vy1**2)
                mag2 = math.sqrt(vx2**2 + vy2**2)

                if mag1 == 0 or mag2 == 0:
                    continue

                coseno = prod / (mag1 * mag2)

                # evitar errores numericos
                coseno = max(-1, min(1, coseno))

                angulo = math.acos(coseno)

                # penalizar angulos menores a 23 grados
                if angulo < math.pi / 8:
                    total += (math.pi / 8 - angulo)

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
        total = 0

        # Desarrolla un criterio propio y ajusta su importancia en el
        # costo total con K4 ¿Mejora el resultado? ¿En que mejora el
        # resultado final?
        #
        # el criterio propio utilizado fue penalizar aristas demasiado
        # largas. para esto se agregó el factor K4 al costo total.
        #
        # este criterio ayudó a que los vértices no quedaran demasiado
        # separados entre sí y permitió obtener grafos visualmente más
        # compactos y organizados.
        #
        # sin este criterio, algunas soluciones reducían cruces pero
        # generaban dibujos muy dispersos o con conexiones demasiado
        # largas, lo que hacía más difícil interpretar el grafo.
        #
        # se utilizó un valor pequeño para K4 porque este criterio solo
        # funciona como un ajuste adicional y no debe ser más importante
        # que minimizar los cruces entre aristas.

        for (v1, v2) in self.aristas:

            x1, y1 = estado_dic[v1]
            x2, y2 = estado_dic[v2]

            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

            if dist > self.dim / 2:
                total += dist / self.dim

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

def calendarizador_lundy_mees(t0, tf, M):
        """
        calendarizador propuesto por lundy y mees (1986).
        la temperatura disminuye en función de sí misma con la fórmula:
        t_k+1 = t_k / (1 + beta * t_k)
        
        el beta se calcula con base en los límites de temperatura y el 
        número de iteraciones máximas (m).
        """
        # calculando el beta a partir de las temperaturas y el numero de iteraciones
        beta = (t0 - tf) / (M * t0 * tf)
        
        t = t0
        while True:
            yield t
            # aplicando la reduccion de temperatura
            t = t / (1.0 + (beta * t))


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

    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    # estado inicial
    estado_aleatorio = grafo_sencillo.estado_aleatorio()

    costo_inicial = grafo_sencillo.costo(estado_aleatorio)

    grafo_sencillo.dibuja_grafo(
        estado_aleatorio,
        "prueba_inicial.gif"
    )

    print("Costo del estado aleatorio: {}".format(costo_inicial))


    t_inicial = time.time()

    solucion_default = blocales.temple_simulado(
        grafo_sencillo
    )

    t_final = time.time()

    costo_default = grafo_sencillo.costo(solucion_default)

    grafo_sencillo.dibuja_grafo(
        solucion_default,
        "prueba_final.gif"
    )

    print("\nUtilizando la calendarización por default")
    print("Costo de la solución encontrada: {}".format(costo_default))
    print("Tiempo de ejecución en segundos: {}".format(
        t_final - t_inicial))

    # calendarizacion Lundy-Mees

    t_inicial = time.time()

    solucion_lundy = blocales.temple_simulado(
        grafo_sencillo,
        calendarizador=calendarizador_lundy_mees(
            t0=400,
            tf=0.01,
            M=15000
        )
    )

    t_final = time.time()

    costo_lundy = grafo_sencillo.costo(solucion_lundy)

    grafo_sencillo.dibuja_grafo(
        solucion_lundy,
        "prueba_lundy.gif"
    )

    print("\nUtilizando calendarizacion Lundy-Mees")
    print("Costo de la solución encontrada: {}".format(
        costo_lundy))
    print("Tiempo de ejecución en segundos: {}".format(
        t_final - t_inicial))

    # grafo feo

    vertices_feo = ['A','B','C','D','E','F','G','H','I']

    aristas_feo = [
    ('A','B'),
    ('A','C'),
    ('A','D'),
    ('B','E'),
    ('B','F'),
    ('C','F'),
    ('C','G'),
    ('D','G'),
    ('D','H'),
    ('E','I'),
    ('F','I'),
    ('G','I'),
    ('H','I'),
    ('B','G'),
    ('C','H'),
    ('D','E')
    ]

    grafo_feo = problema_grafica_grafo(
        vertices_feo,
        aristas_feo,
        dimension
    )

    # estado inicial
    estado_feo = grafo_feo.estado_aleatorio()

    costo_feo_inicial = grafo_feo.costo(estado_feo)

    grafo_feo.dibuja_grafo(
        estado_feo,
        "grafo_feo_inicial.gif"
    )

    print("\nCosto inicial grafo feo: {}".format(
        costo_feo_inicial))


    t_inicial = time.time()

    solucion_feo_default = blocales.temple_simulado(
        grafo_feo
    )

    t_final = time.time()

    costo_feo_default = grafo_feo.costo(
        solucion_feo_default
    )

    grafo_feo.dibuja_grafo(
        solucion_feo_default,
        "grafo_feo_default.gif"
    )

    print("\nGrafo feo con calendarizacion default")
    print("Costo final: {}".format(costo_feo_default))
    print("Tiempo: {}".format(t_final - t_inicial))

    # calendarizacion Lundy-Mees

    t_inicial = time.time()

    solucion_feo_lundy = blocales.temple_simulado(
        grafo_feo,
        calendarizador=calendarizador_lundy_mees(
            t0=500,
            tf=0.01,
            M=14000
        )
    )

    t_final = time.time()

    costo_feo_lundy = grafo_feo.costo(
        solucion_feo_lundy
    )

    grafo_feo.dibuja_grafo(
        solucion_feo_lundy,
        "grafo_feo_lundy.gif"
    )

    print("\nGrafo feo con Lundy-Mees")
    print("Costo final: {}".format(costo_feo_lundy))
    print("Tiempo: {}".format(t_final - t_inicial))

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
    # conclusiones:
    #
    # los valores que dieron mejores resultados fueron temperaturas
    # iniciales relativamente altas y una reducción gradual de la
    # temperatura usando la calendarización de lundy-mees. los
    # parámetros que mejor funcionaron fueron valores cercanos a
    # t0 = 400 o 500 y entre 10000 y 15000 iteraciones, ya que
    # permitieron explorar suficientes estados sin hacer demasiado
    # lento el algoritmo.
    #
    # al comparar los resultados se observó que lundy-mees
    # normalmente encontró soluciones similares o mejores en menos
    # tiempo que la calendarización ya programada. en el grafo
    # sencillo ambos métodos lograron llegar a costo 0.0, pero
    # lundy-mees tardó menos tiempo.
    #
    # en el grafo más complejo la diferencia fue más notable,
    # ya que la versión ya programada tardó bastante más y aun así
    # obtuvo un costo mayor que lundy-mees.
    #
    # el criterio más importante fue el número de cruces entre
    # aristas, porque es lo que más afecta que el grafo se vea
    # claro o desordenado. aun así, agregar criterios como
    # separación entre vértices, ángulos pequeños y longitud de
    # aristas ayudó a que el dibujo final se viera más organizado.
    #
    # también se modificó el método vecino_aleatorio para mover
    # un vértice completo en lugar de solo una coordenada.
    # además, se utilizaron movimientos pequeños más probables
    # usando una distribución gaussiana, lo que ayudó a que el
    # temple simulado hiciera ajustes más estables.
    #
    # finalmente, se creó un grafo más complejo con más conexiones
    # y cruces iniciales. después de aplicar temple simulado se
    # pudo observar una reducción importante en el costo y una
    # mejor distribución de los vértices en el dibujo final.

if __name__ == '__main__':
    main()


"""
Costo del estado aleatorio: 60.9721633042428

Utilizando la calendarización por default
Costo de la solución encontrada: 0.0
Tiempo de ejecución en segundos: 10.679901838302612

Utilizando calendarizacion Lundy-Mees
Costo de la solución encontrada: 0.0
Tiempo de ejecución en segundos: 8.01799750328064

Costo inicial grafo feo: 86.37651906737052

Grafo feo con calendarizacion default
Costo final: 5.095684143885312
Tiempo: 41.79229497909546

Grafo feo con Lundy-Mees
Costo final: 0.22318817904134194
Tiempo: 32.58234691619873
"""