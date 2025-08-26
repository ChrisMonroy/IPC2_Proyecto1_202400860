from ListaSimple import ListaEnlazada
from Campo import Campo
from Estacion import Estacion
from Fre import Frecuencia
from Sensor import Sensor
from xml.dom.minidom import parse

class Sistema:
    def __init__(self):
        self.campos = ListaEnlazada()

    def carga(self, ruta):
        try:
            dom = parse(ruta)
            campoxml = dom.getElementsByTagName('campo')

            for campoxml in campoxml:
                # Crear campo
                id_campo = campoxml.getAttribute('id')
                nombre_campo = campoxml.getAttribute('nombre')
                campo = Campo(id_campo, nombre_campo)
                
                print(f"Cargando campo agricola {id_campo}")
                
                # Cargar estaciones base
                estaciones_xml = campoxml.getElementsByTagName('estacion')
                for estacion_xml in estaciones_xml:
                    id_est = estacion_xml.getAttribute('id')
                    nombre_est = estacion_xml.getAttribute('nombre')
                    estacion = Estacion(id_est, nombre_est)
                    campo.estaciones.insertar(estacion)
                    print(f"Creando estacion base {id_est}")
                
                # Cargar sensores de suelo
                sensores_suelo_xml = campoxml.getElementsByTagName('sensorS')
                for sensor_xml in sensores_suelo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)
                    
                    # Cargar frecuencias
                    frecuencias_xml = sensor_xml.getElementsByTagName('frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    
                    campo.sensores_suelo.insertar(sensor)
                    print(f"Creando sensor de suelo {id_sensor}")
                
                # Cargar sensores de cultivo
                sensores_cultivo_xml = campoxml.getElementsByTagName('sensorT')
                for sensor_xml in sensores_cultivo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)
                    
                    # Cargar frecuencias
                    frecuencias_xml = sensor_xml.getElementsByTagName('frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    
                    campo.sensores_cultivo.insertar(sensor)
                    print(f"Creando sensor de cultivo {id_sensor}")
                
                campo.crear_matrices()
                self.campos.insertar(campo)
            
            print("Archivo cargado exitosamente")
        
        except Exception as ex:
            print(f"Error al cargar archivo: {ex}")

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