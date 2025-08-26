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

            for columnas in range (numero_sensores_cultivo):
                 sensor = self.sensores_cultivo.obtener(columnas)
            actual_frecuencia = sensor.frecuencias.primero
            while actual_frecuencia:
                frecuencia = actual_frecuencia.dato
                num_fila = self.estaciones.buscar_indice(frecuencia.id_estacion)
                if num_fila != -1:
                    self.matriz_cultivo.establecer(num_fila, columnas, frecuencia)
                actual_frecuencia = actual_frecuencia.siguiente

        def mostrar_matriz(self):
         if self.matriz_suelo:
            titulo_suelo = f"Matriz de Suelo - Campo {self.id}"
            self.matriz_suelo.mostrar(titulo_suelo, self.estaciones, self.sensores_suelo)
        
        if self.matriz_cultivo:
            titulo_cultivo = f"Matriz de Cultivo - Campo {self.id}"
            self.matriz_cultivo.mostrar(titulo_cultivo, self.estaciones, self.sensores_cultivo)

    def visualizar_matrices_graphviz(self):
        if self.matriz_suelo:
            print("Generando  Suelo!!!!!")
            self.matriz_suelo.generar_graphviz(
                f"Matriz Suelo - Campo {self.id}",
                self.estaciones,
                self.sensores_suelo,
                f"matriz_suelo_campo_{self.id}"
            )

        if self.matriz_cultivo:
            print("Generando cultivo !!!")
            self.matriz_cultivo.generar_graphviz(
                f"Matriz Cultivo - Campo {self.id}",
                self.estaciones,
                self.sensores_cultivo,
                f"matriz_cultivo_campo_{self.id}"
            )