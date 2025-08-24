from ListaSimple import ListaEnlazada
from Matriz import Matriz

class Campo:
    def __init__ (self, campo, nombre):
        self.campo = campo
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_del_suelo = ListaEnlazada()
        self.sensores_del_cultivo = ListaEnlazada()
        self.matriz_suelo = None
        self.matriz_cultivo = None  

        def CrearMatriz(self):
            numero_estaciones = self.estaciones.longitud
            numero_sensores_suelo = self.sensores_del_suelo.longitud
            numero_sensores_cultivo = self.sensores_del_cultivo.longitud

            self.matriz_suelo = Matriz(numero_estaciones, numero_sensores_suelo)
            self.matriz_cultivo = Matriz(numero_estaciones, numero_sensores_cultivo)

            for columnas in range(numero_sensores_suelo):
                sensor = self.sensores_del_suelo.obtener(columnas)
                frecuencia_actual = sensor.frecuencia.primero
                while frecuencia_actual:
                    frecuencia = frecuencia_actual.dato
                    filas = self.estaciones.buscar_indice(frecuencia.id_estacion)   
                    if filas != -1:
                        self.matriz_suelo.EstablecerFrecuencia(filas, columnas, frecuencia)
                    frecuencia_actual = frecuencia_actual.siguiente

            
