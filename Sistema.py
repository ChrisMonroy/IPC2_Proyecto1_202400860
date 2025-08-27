from ListaSimple import ListaEnlazada
from Campo import Campo
from Estacion import Estacion
from Fre import Frecuencia
from Sensor import Sensor
from xml.dom.minidom import parse

class Sistema:
    def __init__(self):
        self.campos = ListaEnlazada()

    def cargar_archivo(self, ruta_archivo):
        try:
            dom = parse(ruta_archivo)
            campos_xml = dom.getElementsByTagName('campo')
            for campo_xml in campos_xml:
                id_campo = campo_xml.getAttribute('id')
                nombre_campo = campo_xml.getAttribute('nombre')
                campo = Campo(id_campo, nombre_campo)
                print(f"Cargando campo agricola {id_campo}")

                estaciones_xml = campo_xml.getElementsByTagName('estacion')
                for estacion_xml in estaciones_xml:
                    id_est = estacion_xml.getAttribute('id')
                    nombre_est = estacion_xml.getAttribute('nombre')
                    estacion = Estacion(id_est, nombre_est)
                    campo.estaciones.insertar(estacion)
                    print(f"Creando estacion base {id_est}")

                sensores_suelo_xml = campo_xml.getElementsByTagName('sensorS')
                for sensor_xml in sensores_suelo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)
                    frecuencias_xml = sensor_xml.getElementsByTagName('frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data.strip()
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    campo.sensores_del_suelo.insertar(sensor)
                    print(f"Creando sensor de suelo {id_sensor}")

                sensores_cultivo_xml = campo_xml.getElementsByTagName('sensorT')
                for sensor_xml in sensores_cultivo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)
                    frecuencias_xml = sensor_xml.getElementsByTagName('frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data.strip()
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    campo.sensores_del_cultivo.insertar(sensor)
                    print(f"Creando sensor de cultivo {id_sensor}")

                campo.crear_matrices()
                self.campos.insertar(campo)

            print("Archivo cargado exitosamente")

        except Exception as e:
            print(f"Error al cargar archivo: {e}")

    def listar_campos(self):
        print("\nCampos Disponibles:")
        print("-" * 25)
        actual = self.campos.primero
        while actual:
            campo = actual.dato
            print(f"ID: {campo.id} - {campo.nombre}")
            actual = actual.siguiente

    def mostrar_campo(self, id_campo):
        actual = self.campos.primero
        while actual:
            campo = actual.dato
            if campo.id == id_campo:
                campo.mostrar_matrices()
                return
            actual = actual.siguiente
        print(f"Campo {id_campo} no encontrado")

    def generar_salida_xml(self, ruta_salida):
        from xml.dom.minidom import Document
        doc = Document()
        root = doc.createElement("camposAgricolas")
        doc.appendChild(root)

        actual = self.campos.primero
        while actual:
            campo = actual.dato
            campo_elem = doc.createElement("campo")
            campo_elem.setAttribute("id", campo.id)
            campo_elem.setAttribute("nombre", campo.nombre)

            er_elem = doc.createElement("estacionesBaseReducidas")
            grupos = campo.agrupar_estaciones()
            for idx, grupo in enumerate(grupos):
                e = doc.createElement("estacion")
                e.setAttribute("id", f"er{idx+1}")
                e.setAttribute("nombre", ", ".join(grupo))
                er_elem.appendChild(e)
            campo_elem.appendChild(er_elem)

            ss_elem = doc.createElement("sensoresSuelo")
            for j in range(campo.sensores_del_suelo.longitud):
                sensor = campo.sensores_del_suelo.obtener(j)
                s_elem = doc.createElement("sensorS")
                s_elem.setAttribute("id", sensor.sensor)
                s_elem.setAttribute("nombre", sensor.nombre)
                for idx, grupo in enumerate(grupos):
                    suma = 0
                    for id_est in grupo:
                        i_orig = campo.estaciones.buscar_indice(id_est)
                        freq = campo.matriz_suelo.ObtenerFrecuencia(i_orig, j)
                        if freq:
                            suma += freq.valor
                    if suma > 0:
                        f_elem = doc.createElement("frecuencia")
                        f_elem.setAttribute("idEstacion", f"er{idx+1}")
                        f_elem.appendChild(doc.createTextNode(str(suma)))
                        s_elem.appendChild(f_elem)
                ss_elem.appendChild(s_elem)
            campo_elem.appendChild(ss_elem)

            st_elem = doc.createElement("sensoresCultivo")
            for j in range(campo.sensores_del_cultivo.longitud):
                sensor = campo.sensores_del_cultivo.obtener(j)
                s_elem = doc.createElement("sensorT")
                s_elem.setAttribute("id", sensor.sensor)
                s_elem.setAttribute("nombre", sensor.nombre)
                for idx, grupo in enumerate(grupos):
                    suma = 0
                    for id_est in grupo:
                        i_orig = campo.estaciones.buscar_indice(id_est)
                        freq = campo.matriz_cultivo.ObtenerFrecuencia(i_orig, j)
                        if freq:
                            suma += freq.valor
                    if suma > 0:
                        f_elem = doc.createElement("frecuencia")
                        f_elem.setAttribute("idEstacion", f"er{idx+1}")
                        f_elem.appendChild(doc.createTextNode(str(suma)))
                        s_elem.appendChild(f_elem)
                    st_elem.appendChild(s_elem)
                campo_elem.appendChild(st_elem)

            root.appendChild(campo_elem)
            actual = actual.siguiente

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))
        print(f"Archivo de salida generado: {ruta_salida}")