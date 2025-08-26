from Sistema import Sistema
from Campo import Campo
from Matriz import Matriz
from ListaSimple import ListaEnlazada

def main():
    sistema = Sistema()
    
    while True:
        print("-" * 100)
        print(" SISTEMA DE AGRICULTURA DE PRECISION ")
        print("1. Cargar archivo                    ")
        print("2. Mostrar matrices                  ")
        print("3. Graficar matrices                 ")
        print("4. Mostrar información del autor     ")
        print("5. Mostrar Grafica                    ")
        print("6. Salir                             ")
        print("-" * 100)
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            print("\nCargar archivo:")
            ruta = input("Ingrese la ruta del archivo: ")
            nombre = input("Ingrese el nombre del archivo: ")
            archivo = ruta + "/" + nombre if ruta else nombre
            sistema.cargar_archivo(archivo)

        elif opcion == "2":
            print("\nMostrar matrices:")
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ")
            sistema.mostrar_campo(id_campo)

        elif opcion == "3":
            print("\nGraficar matrices con Graphviz:")
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ")

            # Buscar el campo y graficar
            actual = sistema.campos.primero
            encontrado = False
            while actual:
                campo = actual.dato
                if campo.id == id_campo:
                    campo.matriz_suelo.generar_graphviz_tabla(
                        f"Matriz de Suelo - Campo {campo.id}",
                        campo.estaciones,
                        campo.sensores_suelo,
                        f"matriz_suelo_tabla_campo_{campo.id}"
                    )
                    encontrado = True
                    break
                actual = actual.siguiente
            if not encontrado:
                print(f"Campo {id_campo} no encontrado")

        elif opcion == "5":
         print("GENERAR GRÁFICA")
        sistema.listar_campos()
        id_campo = input("Ingrese el ID del campo: ")
        tipo = input("Tipo de matriz (frecuencia, patron, reducida): ")

        campo = sistema.buscar_campo(id_campo)
        if not campo:
            print("Campo no encontrado")
            continue

        if tipo == "frecuencia":
            campo.matriz_suelo.Graficar("Matriz Frecuencia Suelo", campo.estaciones, campo.sensores_del_suelo, f"fs_{id_campo}")
            campo.matriz_cultivo.Graficar("Matriz Frecuencia Cultivo", campo.estaciones, campo.sensores_del_cultivo, f"ft_{id_campo}")
        elif tipo == "patron":
            # Mostrar patrón como tabla con valores 0/1 o frecuencias normalizadas
            pass  # Puedes usar la misma función Graficar()
        elif tipo == "reducida":
            if hasattr(campo, 'matriz_suelo_reducida'):
                campo.matriz_suelo_reducida.Graficar("Matriz Reducida Suelo", ListaEnlazada(), campo.sensores_del_suelo, f"frs_{id_campo}")
            if hasattr(campo, 'matriz_cultivo_reducida'):
                campo.matriz_cultivo_reducida.Graficar("Matriz Reducida Cultivo", ListaEnlazada(), campo.sensores_del_cultivo, f"frt_{id_campo}")

        elif opcion == "6":
         print("SALIENDO DEL PROGRAMA!!!!")

        elif opcion == "4":
         print("="*50)
        print("Nombre: Christopher Alejandro Monroy Maldonado")
        print("Carné: 202400860")
        print("Curso: Introducción a la Programación y Computación 2")
        print("Carrera: Ingeniería en Ciencias y Sistemas")
        print("="*50)

    else:
        print("Opcion no valida")

if __name__ == "__main__":
    main()