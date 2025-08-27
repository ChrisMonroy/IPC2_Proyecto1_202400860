from Sistema import Sistema
from ListaSimple import ListaEnlazada
import tkinter as tk
from tkinter import filedialog

def main():
    sistema = Sistema()

    # Ocultar ventana principal de Tkinter
    root = tk.Tk()
    root.withdraw()

    while True:
        print("\n" + "=" * 100)
        print("           SISTEMA DE AGRICULTURA DE PRECISION")
        print("=" * 100)
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo de salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salir")
        print("=" * 100)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n¿Cómo desea cargar el archivo?")
            print("1. Ingresar ruta y nombre manualmente")
            print("2. Usar explorador de archivos")
            sub_opcion = input("Seleccione una opción: ").strip()

            if sub_opcion == "1":
                ruta = input("Ingrese la ruta del archivo: ").strip()
                nombre = input("Ingrese el nombre del archivo: ").strip()
                ruta_archivo = ruta + "/" + nombre if ruta else nombre
            elif sub_opcion == "2":
                print("Abriendo explorador de archivos...")
                ruta_archivo = filedialog.askopenfilename(
                    title="Seleccionar archivo XML",
                    filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
                )
                if not ruta_archivo:
                    print("No se seleccionó ningún archivo.")
                    continue
            else:
                print("Opción no válida.")
                continue

            nombre_archivo = ruta_archivo.split("/")[-1] if "/" in ruta_archivo else ruta_archivo.split("\\")[-1]
            print(f"Archivo seleccionado: {nombre_archivo}")
            sistema.cargar_archivo(ruta_archivo)

        elif opcion == "2":
            print("\nProcesando archivo...")
            actual = sistema.campos.primero
            if actual is None:
                print("No hay campos cargados. Cargue un archivo primero.")
                continue
            while actual:
                campo = actual.dato
                print(f"Procesando campo {campo.id}...")
                campo.crear_matrices()
                campo.agrupar_estaciones()
                campo.crear_matrices_reducidas()
                campo.mostrar_matrices()
                actual = actual.siguiente
            print("Todos los campos han sido procesados.")

        elif opcion == "3":
            print("\nEscribir archivo de salida:")
            ruta_salida = filedialog.asksaveasfilename(
                title="Guardar archivo de salida",
                filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")],
                defaultextension=".xml"
            )
            if ruta_salida:
                sistema.generar_salida_xml(ruta_salida)
            else:
                print("No se seleccionó una ruta de guardado.")

        elif opcion == "4":
            print("\n" + "=" * 50)
            print("Nombre: Christopher Alejandro Monroy Maldonado")
            print("Carné: 202400860")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Carrera: Ingeniería en Ciencias y Sistemas")
            print("GitHub: https://github.com/ChrisMonroy/Proyecto1_IPC2")
            print("=" * 50)

        elif opcion == "5":
            print("\nGENERAR GRÁFICA CON GRAPHVIZ")
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ").strip()
            tipo = input("Tipo de gráfica (frecuencia, reducida): ").strip().lower()

            actual = sistema.campos.primero
            encontrado = False
            while actual:
                campo = actual.dato
                if campo.id == id_campo:
                    if tipo == "frecuencia":
                        if campo.matriz_suelo:
                            campo.matriz_suelo.Graficar(
                                f"Matriz Frecuencia Suelo - Campo {id_campo}",
                                campo.estaciones,
                                campo.sensores_del_suelo,
                                f"fs_{id_campo}"
                            )
                        if campo.matriz_cultivo:
                            campo.matriz_cultivo.Graficar(
                                f"Matriz Frecuencia Cultivo - Campo {id_campo}",
                                campo.estaciones,
                                campo.sensores_del_cultivo,
                                f"ft_{id_campo}"
                            )
                    elif tipo == "reducida":
                        if hasattr(campo, 'matriz_suelo_reducida') and campo.matriz_suelo_reducida:
                            campo.matriz_suelo_reducida.Graficar(
                                f"Matriz Reducida Suelo - Campo {id_campo}",
                                ListaEnlazada(),
                                campo.sensores_del_suelo,
                                f"frs_{id_campo}"
                            )
                        if hasattr(campo, 'matriz_cultivo_reducida') and campo.matriz_cultivo_reducida:
                            campo.matriz_cultivo_reducida.Graficar(
                                f"Matriz Reducida Cultivo - Campo {id_campo}",
                                ListaEnlazada(),
                                campo.sensores_del_cultivo,
                                f"frt_{id_campo}"
                            )
                    else:
                        print("Tipo no válido. Use: frecuencia o reducida")
                    encontrado = True
                    break
                actual = actual.siguiente

            if not encontrado:
                print(f"Campo {id_campo} no encontrado")

        elif opcion == "6":
            print("Saliendo del programa... ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()