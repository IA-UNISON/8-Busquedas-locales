"""
blocales.py
------------

Algoritmos generales para búsquedas locales

"""

from abc import ABC, abstractmethod
from itertools import takewhile
from math import exp
from random import random
import random
import math

class Problema(ABC):
    """
    Definición formal de un problema de búsqueda local. Es necesario
    adaptarla a cada problema en específico, en particular:

    a) Todos los métodos requieren de implementar costo y estado_aleatorio

    b) descenso_colinas  requiere de implementar el método vecinos

    c) temple_simulado requiere vecino_aleatorio

    """
    @abstractmethod
    def estado_aleatorio(self):
        """
        @return Una tupla que describe un estado

        """
        raise NotImplementedError("Este metodo debe ser implementado")

    @abstractmethod
    def vecinos(self, estado):
        """
        Generador de los vecinos de un estado

        @param estado: Una tupla que describe un estado

        @return: Un generador de estados vecinos

        """
        raise NotImplementedError("Este metodo debe ser implementado")

    @abstractmethod
    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado en forma aleatoria.
        Procurar generar el estado  vecino a partir de una
        distribución uniforme de ser posible.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.
        """
        raise NotImplementedError("Este metodo debe ser implementado")

    @abstractmethod
    def costo(self, estado):
        """
        Calcula el costo de un estado dado

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        raise NotImplementedError("Este metodo debe ser implementado")


def descenso_colinas(problema, maxit=1e6):
    """
    Busqueda local por descenso de colinas.

    @param problema: Un objeto de una clase heredada de Problema
    @param maxit: Máximo número de iteraciones

    @return: El estado con el menor costo encontrado

    """
    estado = problema.estado_aleatorio()
    costo = problema.costo(estado)

    for _ in range(int(maxit)):
        e = min(problema.vecinos(estado), key=problema.costo)
        c = problema.costo(e)
        if c >= costo:
            break
        estado, costo = e, c
    return estado


#def temple_simulado(problema, calendarizador=None, tol=0.001):
    #"""
    #Busqueda local por temple simulado
#
    #@param problema: Un objeto de la clase `Problema`.
    #@param calendarizador: Un generador de temperatura (simulación).
    #@param tol: Temperatura mínima considerada diferente a cero.
#
    #@return: El estado con el menor costo encontrado
#
    #"""
    #if calendarizador is None:
        #costos = [
            #problema.costo(problema.estado_aleatorio())
            #for _ in range(10 * len(problema.estado_aleatorio()))
        #]
        #minimo,  maximo = min(costos), max(costos)
        #T_ini = 2 * (maximo - minimo)
        #calendarizador = (T_ini/(1 + i) for i in range(int(1e10)))
#
    #estado = problema.estado_aleatorio()
    #costo = problema.costo(estado)
#
    #for T in takewhile(lambda i: i > tol, calendarizador):
#
        #vecino = problema.vecino_aleatorio(estado)
        #costo_vecino = problema.costo(vecino)
        #incremento_costo = costo_vecino - costo
#
        #if incremento_costo <= 0 or random() < exp(-incremento_costo / T):
            #estado, costo = vecino, costo_vecino
    #return estado


def temple_simulado(problema, 
                          temp_inicial=1.0, 
                          temp_final=0.01, 
                          factor_enfriamiento=0.95,
                          max_iter=1000000,
                          max_iter_temp=100,
                          max_exitos=10,
                          factor_adaptativo=True,
                          dmax_inicial=10):
    """
    Implementación de temple simulado que utiliza factores adaptativos
    tanto para la temperatura como para la generación de vecinos.
    
    @param problema: Instancia de la clase con los métodos requeridos
    @param temp_inicial: Temperatura inicial
    @param temp_final: Temperatura final
    @param factor_enfriamiento: Factor de reducción de temperatura
    @param max_iter: Número máximo de iteraciones totales
    @param max_iter_temp: Máximo de iteraciones por temperatura
    @param max_exitos: Máximo de éxitos por temperatura antes de enfriar
    @param factor_adaptativo: Si es True, adapta la calendarización según el progreso
    @param dmax_inicial: Valor inicial para el parámetro dmax del vecino aleatorio
    
    @return: El estado correspondiente a la mejor solución encontrada
    """
    # Inicializa el estado actual como aleatorio y calcula su costo
    estado_actual = problema.estado_aleatorio()
    costo_actual = problema.costo(estado_actual)
    
    # Guarda el mejor estado y su costo
    mejor_estado = estado_actual
    mejor_costo = costo_actual
    
    # Inicialización de variables para estadísticas y control
    iteracion = 0
    temp = temp_inicial
    
    # Variables para adaptación
    exitos_temp = 0  # Número de éxitos por temperatura
    mejoras_temp = 0  # Número de mejoras por temperatura
    dmax = dmax_inicial  # Amplitud de movimientos
    
    # Historial para detectar estancamiento
    historial_costos = []
    
    # Configuración de temperatura adaptativa al problema
    if costo_actual > 1:
        # Si los costos son altos, ajustar la temperatura inicial
        temp_inicial = costo_actual / 10
        temp = temp_inicial
    
    # Continuar mientras no se alcance la temperatura mínima y queden iteraciones
    while temp > temp_final and iteracion < max_iter:
        
        # Almacenar estadísticas para esta temperatura
        exitos_temp = 0
        mejoras_temp = 0
        iteraciones_temp = 0
        
        # Normalizar el factor de temperatura para pasarlo al vecino aleatorio
        temp_factor = (temp - temp_final) / (temp_inicial - temp_final)
        temp_factor = max(0.0, min(1.0, temp_factor))  # Asegurar que esté entre 0 y 1
        
        # Establecer el temp_factor como atributo del problema para que vecino_aleatorio lo use
        setattr(problema, 'temp_factor', temp_factor)
        
        # Realizar iteraciones para la temperatura actual
        while iteraciones_temp < max_iter_temp and exitos_temp < max_exitos:
            iteraciones_temp += 1
            iteracion += 1
            
            # Generar vecino con el factor de temperatura actual
            vecino = problema.vecino_aleatorio(estado_actual, dmax=dmax, temp_factor=temp_factor)
            costo_vecino = problema.costo(vecino)
            
            # Calcular delta de costo
            delta = costo_vecino - costo_actual
            
            # Decidir si aceptar el vecino (siempre si es mejor, probabilísticamente si es peor)
            if delta < 0 or random.random() < math.exp(-delta / temp):
                estado_actual = vecino
                costo_actual = costo_vecino
                exitos_temp += 1
                
                # Si encontramos un nuevo mejor estado
                if costo_actual < mejor_costo:
                    mejor_estado = estado_actual
                    mejor_costo = costo_actual
                    mejoras_temp += 1
            
            # Imprimir progreso cada cierto número de iteraciones
            if iteracion % 1000 == 0:
                print(f"Iteración {iteracion}, Temperatura: {temp:.4f}, Mejor costo: {mejor_costo:.4f}")
        
        # Ajustar parámetros adaptativos basados en los resultados de esta temperatura
        if factor_adaptativo:
            # Ajustar el factor de enfriamiento
            if mejoras_temp > 0:
                # Si hubo mejoras, enfriar más lentamente
                factor_enfriamiento_actual = min(0.98, factor_enfriamiento * 1.05)
            elif exitos_temp < max_exitos * 0.3:
                # Si hubo pocos éxitos, enfriar más rápidamente
                factor_enfriamiento_actual = max(0.8, factor_enfriamiento * 0.95)
            else:
                factor_enfriamiento_actual = factor_enfriamiento
            
            # Ajustar dmax (amplitud de movimientos)
            if exitos_temp < max_exitos * 0.2:
                # Si hay muy pocos éxitos, aumentar la amplitud para explorar más
                dmax = min(30, dmax * 1.2)
            elif exitos_temp > max_exitos * 0.8:
                # Si hay muchos éxitos, reducir la amplitud para refinar
                dmax = max(1, dmax * 0.8)
        else:
            factor_enfriamiento_actual = factor_enfriamiento
        
        # Almacenar costo para detectar estancamiento
        historial_costos.append(mejor_costo)
        
        # Verificar estancamiento (últimas 5 temperaturas sin mejora significativa)
        if len(historial_costos) > 5:
            ultimos_costos = historial_costos[-5:]
            variacion = max(ultimos_costos) - min(ultimos_costos)
            
            # Si estamos estancados, podemos:
            if variacion < 0.001 * min(ultimos_costos):
                # 1. Hacer un enfriamiento más rápido
                factor_enfriamiento_actual = 0.7
                # 2. O calentar de nuevo el sistema (opción más drástica)
                if random.random() < 0.2:  # 20% de probabilidad
                    temp = temp_inicial * 0.5  # Recalentar a 50% de temp inicial
                    print("Recalentando sistema por estancamiento")
                    continue  # Saltar el enfriamiento
        
        # Actualizar temperatura según el esquema de enfriamiento
        temp *= factor_enfriamiento_actual
        
        # Imprimir estadísticas de esta fase
        print(f"Temperatura: {temp:.6f}, Éxitos: {exitos_temp}/{iteraciones_temp}, " +
              f"Mejoras: {mejoras_temp}, Factor: {factor_enfriamiento_actual:.3f}, dmax: {dmax}")
    
    print(f"\nProceso terminado después de {iteracion} iteraciones")
    print(f"Mejor costo encontrado: {mejor_costo}")
    
    return mejor_estado
