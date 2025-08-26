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

    def generar_patron(self):
        patron = ""
        for i in range(self.filas):
            for j in range(self.columnas):
                freq = self.obtener_frecuencia(i, j)
                valor = freq.valor if freq else 0
                patron += str(valor) + "_"
            patron = patron.rstrip("_") + "|"
        return patron.rstrip("|")

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

        filas_html = ""
        for i in range(self.filas):
           estacion = encabezado_filas.obtener(i)
           filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion.id)}</b></td>'
        for j in range(self.columnas):
            frecuencia = self.ObtenerFrecuencia(i, j)
            valor = esc(frecuencia.valor)
            # Color de celda según valor
            bg = "#ffffff" if valor == "0" else "#ffd6d6"  # blanco=0, rosado=>0 (ajustable)
            filas_html += f'<td border="1" bgcolor="{bg}">{valor}</td>'
        filas_html += '</tr>'

        # Armar tabla HTML-like
        tabla = f'''
          <<table BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <tr><td>
          <table BORDER="1" CELLBORDER="1" CELLSPACING="0">
          <tr>{th_cols}</tr>
              {filas_html}
          </table>
          </td></tr>
          </table>>
        '''

        dot = graphviz.Digraph(comment=str(titulo))
        dot.attr(rankdir='LR')
        # Usamos shape=plain para que respete el label HTML
        dot.node('matriz_tabla', label=tabla, shape='plain')

         # Título como nodo separado arriba (opcional)
        dot.node('titulo', label=str(titulo), shape='box', style='filled', fillcolor='lightgreen')
        dot.edge('titulo', 'matriz_tabla', style='invis')  # invisible para ordenar verticalmente

         # Guardar DOT en UTF-8
        with open(f'{nombre_archivo}.dot', 'w', encoding='utf-8') as f:
             f.write(dot.source)

        print(f"Archivo DOT generado: {nombre_archivo}.dot")
        print(f"Para generar PNG: dot -Tpng {nombre_archivo}.dot -o {nombre_archivo}.png")
        return dot.source