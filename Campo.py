from Fre import Frecuencia
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

        def crearMatriz(self):
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

    def agrupar_estaciones(self):
        patrones_suelo = {}
        patrones_cultivo = {}

        # Obtener patrón por estación para suelo
        for i in range(self.estaciones.longitud):
            estacion = self.estaciones.obtener(i)
            fila_suelo = ""
            for j in range(self.sensores_del_suelo.longitud):
                freq = self.matriz_suelo.obtener_frecuencia(i, j)
                fila_suelo += f"{freq.valor if freq else 0}_"
            patrones_suelo[estacion.id_estacion] = fila_suelo.rstrip("_")

        # Obtener patrón por estación para cultivo
        for i in range(self.estaciones.longitud):
            estacion = self.estaciones.obtener(i)
            fila_cultivo = ""
            for j in range(self.sensores_del_cultivo.longitud):
                freq = self.matriz_cultivo.obtener_frecuencia(i, j)
                fila_cultivo += f"{freq.valor if freq else 0}_"
            patrones_cultivo[estacion.id_estacion] = fila_cultivo.rstrip("_")

        # Agrupar
        grupos = {}
        for id_est in patrones_suelo:
            key = f"{patrones_suelo[id_est]}|{patrones_cultivo[id_est]}"
            if key not in grupos:
                grupos[key] = []
            grupos[key].append(id_est)

        return list(grupos.values())
    
    def crear_matrices_reducidas(self):
        grupos = self.agrupar_estaciones()
        n_grupos = len(grupos)
        n_sensores_s = self.sensores_del_suelo.longitud
        n_sensores_t = self.sensores_del_cultivo.longitud

        self.matriz_suelo_reducida = Matriz(n_grupos, n_sensores_s)
        self.matriz_cultivo_reducida = Matriz(n_grupos, n_sensores_t)

        # Mapeo: estación → grupo
        grupo_de_estacion = {}
        for idx, grupo in enumerate(grupos):
            for id_est in grupo:
                grupo_de_estacion[id_est] = idx

        # Sumar frecuencias
        for i in range(self.estaciones.longitud):
            estacion = self.estaciones.obtener(i)
            grupo_idx = grupo_de_estacion[estacion.id_estacion]

            for j in range(n_sensores_s):
                freq = self.matriz_suelo.obtener_frecuencia(i, j)
                if freq and freq.valor > 0:
                    actual = self.matriz_suelo_reducida.obtener_frecuencia(grupo_idx, j)
                    if actual and actual.valor != 0:
                        actual.valor += freq.valor
                    else:
                        self.matriz_suelo_reducida.establecer_frecuencia(grupo_idx, j, Frecuencia(estacion.id_estacion, str(freq.valor)))
            for j in range(n_sensores_t):
                freq = self.matriz_cultivo.obtener_frecuencia(i, j)
                if freq and freq.valor > 0:
                    actual = self.matriz_cultivo_reducida.obtener_frecuencia(grupo_idx, j)
                    if actual and actual.valor != 0:
                        actual.valor += freq.valor
                    else:
                        self.matriz_cultivo_reducida.establecer_frecuencia(grupo_idx, j, Frecuencia(estacion.id_estacion, str(freq.valor)))

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