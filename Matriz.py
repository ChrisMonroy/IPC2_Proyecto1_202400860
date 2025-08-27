from ListaSimple import ListaEnlazada
from Fre import Frecuencia
import graphviz

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = ListaEnlazada()
        for i in range(filas):
            fila = ListaEnlazada()
            for j in range(columnas):
                frecuencia = Frecuencia("", "0")
                fila.insertar(frecuencia)
            self.matriz.insertar(fila)

    def EstablecerFrecuencia(self, fila, columna, frecuencia):
        fila_lista = self.matriz.obtener(fila)
        if fila_lista:
            nodo = fila_lista.primero
            for _ in range(columna):
                if nodo:
                    nodo = nodo.siguiente
            if nodo:
                nodo.dato = frecuencia

    def ObtenerFrecuencia(self, fila, columna):
        fila_lista = self.matriz.obtener(fila)
        if fila_lista:
            return fila_lista.obtener(columna)
        return None

    def MostrarMatriz(self, titulo, encabezado_filas, encabezado_columnas):
        print(titulo)
        print("=" * 50)
        print("Estación", end="\t")
        for j in range(self.columnas):
            sensor = encabezado_columnas.obtener(j)
            print(f"{sensor.sensor}", end="\t")
        print()
        print("-" * 50)
        for i in range(self.filas):
            estacion = encabezado_filas.obtener(i)
            print(f"{estacion.id_estacion}", end="\t\t")
            for j in range(self.columnas):
                frecuencia = self.ObtenerFrecuencia(i, j)
                valor = frecuencia.valor if frecuencia else 0
                print(f"{valor}", end="\t")
            print()
        print("=" * 50)

    def Graficar(self, titulo, encabezado_filas, encabezado_columnas, nombre_archivo="matriz_tabla"):
        def esc(s):
            return str(s).replace('"', '\\"').replace('<', '<').replace('>', '>')

        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'
        for j in range(self.columnas):
            sensor = encabezado_columnas.obtener(j) if encabezado_columnas else None
            sensor_id = sensor.sensor if sensor else f"Sensor_{j+1}"
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor_id)}</b></td>'

        filas_html = ""
        for i in range(self.filas):
            estacion = encabezado_filas.obtener(i) if encabezado_filas else None
            estacion_id = estacion.id_estacion if estacion else f"Est_{i+1}"
            filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion_id)}</b></td>'
            for j in range(self.columnas):
                frecuencia = self.ObtenerFrecuencia(i, j)
                valor = esc(frecuencia.valor) if frecuencia else "0"
                bg_color = "#ffffff" if valor == "0" else "#ffd6d6"
                filas_html += f'<td border="1" bgcolor="{bg_color}">{valor}</td>'
            filas_html += '</tr>'

        tabla_html = f'''
        <<table BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <tr>{th_cols}</tr>
        {filas_html}
        </table>>
        '''

        dot = graphviz.Digraph(comment=str(titulo))
        dot.attr(rankdir='LR')
        dot.node('tabla', label=tabla_html, shape='plaintext')
        dot.node('titulo', label=str(titulo), shape='box', style='filled', fillcolor='lightblue')
        dot.edge('titulo', 'tabla', style='invis')

        try:
            dot.render(filename=nombre_archivo, format='png', cleanup=True)
            print(f"Imagen generada: {nombre_archivo}.png")
        except Exception as e:
            print(f"Error al generar la imagen: {e}")