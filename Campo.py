from ListaSimple import ListaEnlazada
from Matriz import Matriz
from Fre import Frecuencia

class Campo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_del_suelo = ListaEnlazada()
        self.sensores_del_cultivo = ListaEnlazada()
        self.matriz_suelo = None
        self.matriz_cultivo = None
        self.matriz_suelo_reducida = None
        self.matriz_cultivo_reducida = None

    def crear_matrices(self):
        num_estaciones = self.estaciones.longitud
        num_sensores_suelo = self.sensores_del_suelo.longitud
        num_sensores_cultivo = self.sensores_del_cultivo.longitud

        self.matriz_suelo = Matriz(num_estaciones, num_sensores_suelo)
        self.matriz_cultivo = Matriz(num_estaciones, num_sensores_cultivo)

        for j in range(num_sensores_suelo):
            sensor = self.sensores_del_suelo.obtener(j)
            actual_freq = sensor.frecuencias.primero
            while actual_freq:
                freq = actual_freq.dato
                i = self.estaciones.buscar_indice(freq.id)
                if i != -1:
                    self.matriz_suelo.EstablecerFrecuencia(i, j, freq)
                actual_freq = actual_freq.siguiente

        for j in range(num_sensores_cultivo):
            sensor = self.sensores_del_cultivo.obtener(j)
            actual_freq = sensor.frecuencias.primero
            while actual_freq:
                freq = actual_freq.dato
                i = self.estaciones.buscar_indice(freq.id)
                if i != -1:
                    self.matriz_cultivo.EstablecerFrecuencia(i, j, freq)
                actual_freq = actual_freq.siguiente

    def mostrar_matrices(self):
        if self.matriz_suelo:
            self.matriz_suelo.MostrarMatriz(
                f"Matriz de Suelo - Campo {self.id}",
                self.estaciones,
                self.sensores_del_suelo
            )
        if self.matriz_cultivo:
            self.matriz_cultivo.MostrarMatriz(
                f"Matriz de Cultivo - Campo {self.id}",
                self.estaciones,
                self.sensores_del_cultivo
            )

    def agrupar_estaciones(self):
        patrones_suelo = {}
        patrones_cultivo = {}

        for i in range(self.estaciones.longitud):
            estacion = self.estaciones.obtener(i)
            key_suelo = ""
            key_cultivo = ""
            for j in range(self.sensores_del_suelo.longitud):
                freq = self.matriz_suelo.ObtenerFrecuencia(i, j)
                key_suelo += f"{freq.valor if freq else 0}_"
            for j in range(self.sensores_del_cultivo.longitud):
                freq = self.matriz_cultivo.ObtenerFrecuencia(i, j)
                key_cultivo += f"{freq.valor if freq else 0}_"
            key = f"{key_suelo}|{key_cultivo}"
            if key not in patrones_suelo:
                patrones_suelo[key] = []
            patrones_suelo[key].append(estacion.id_estacion)
        return list(patrones_suelo.values())

    def crear_matrices_reducidas(self):
        grupos = self.agrupar_estaciones()
        n_grupos = len(grupos)
        n_sensores_s = self.sensores_del_suelo.longitud
        n_sensores_t = self.sensores_del_cultivo.longitud

        self.matriz_suelo_reducida = Matriz(n_grupos, n_sensores_s)
        self.matriz_cultivo_reducida = Matriz(n_grupos, n_sensores_t)

        grupo_de_estacion = {}
        for idx, grupo in enumerate(grupos):
            for id_est in grupo:
                grupo_de_estacion[id_est] = idx

        for i in range(self.estaciones.longitud):
            estacion = self.estaciones.obtener(i)
            grupo_idx = grupo_de_estacion[estacion.id_estacion]
            for j in range(n_sensores_s):
                freq = self.matriz_suelo.ObtenerFrecuencia(i, j)
                if freq and freq.valor > 0:
                    actual = self.matriz_suelo_reducida.ObtenerFrecuencia(grupo_idx, j)
                    if actual and actual.valor != 0:
                        actual.valor += freq.valor
                    else:
                        nueva = Frecuencia(estacion.id_estacion, str(freq.valor))
                        self.matriz_suelo_reducida.EstablecerFrecuencia(grupo_idx, j, nueva)
            for j in range(n_sensores_t):
                freq = self.matriz_cultivo.ObtenerFrecuencia(i, j)
                if freq and freq.valor > 0:
                    actual = self.matriz_cultivo_reducida.ObtenerFrecuencia(grupo_idx, j)
                    if actual and actual.valor != 0:
                        actual.valor += freq.valor
                    else:
                        nueva = Frecuencia(estacion.id_estacion, str(freq.valor))
                        self.matriz_cultivo_reducida.EstablecerFrecuencia(grupo_idx, j, nueva)