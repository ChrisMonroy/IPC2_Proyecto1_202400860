from ListaSimple import ListaEnlazada
from Fre import Frecuencia

class Matriz:
    def __init__ (self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = ListaEnlazada()

        for i in range(filas):
            fila = ListaEnlazada()
            for j in range(columnas):
                frecuencia = Frecuencia("", "0")
                fila.insertar(frecuencia)
            self.matriz.insertar(fila)

    def EstablecerFrecuencia(self, filas, columnas, frecuencia):
        fila = self.matriz.obtener(filas)
        if fila:
            # Buscar el nodo en la columna especifica
            columna = fila.primero
            for i in range(columnas):
                if columna:
                    columna = columna.siguiente
            if columna:
                columna.dato = frecuencia

    def ObtenerFrecuencia(self, filas, columnas):
        filas = self.matriz.obtener(filas)
        if filas:
            return filas.obtener(columnas)
        return None

    def MostrarMatriz(self, titulo, encabezado_filas, encabezado_columnas):
        print(titulo)
        print("=" * 30)
        print("Estacion")
        print("=" * 30)
        for j in range(self.columnas):
            sensor = encabezado_columnas.obtener(j)
            print(f"{sensor.id}", end="\t")

            for i in range(self.filas):
                estacion = encabezado_filas.obtener(i)
                print(f"{estacion.id}", end="\t\t")
                for j in range(self.columnas):
                    frecuencia = self.ObtenerFrecuencia(i, j)
                    print(f"{frecuencia.valor}", end="\t")

    def Graficar(self, titulo, encabezado_filas, encabezado_columnas, nombre_archivo = "matriz_tabla"):
        import graphviz

        def esc(s):
            # Escapa comillas y asegura str
            return str(s).replace('"', '\\"')

        # Construir cabecera de columnas
        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'  # celda vacía de esquina
        for j in range(self.columnas):
            sensor = encabezado_columnas.obtener(j)
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor.id)}</b></td>'