import os
import subprocess
import json # Importamos el módulo json para guardar y cargar datos

# --- Configuración para la persistencia de tareas ---
# Nombre del archivo donde se guardarán las tareas
TAREAS_FILE = "tareas_poo.json"

# --- Funciones de Utilidad Existentes ---

def mostrar_codigo(ruta_script):
    """
    Muestra el contenido de un archivo de script Python.
    """
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo: # Añadido encoding para evitar errores
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    """
    Ejecuta un script Python en una nueva ventana de terminal.
    Se adapta a sistemas Windows y Unix-based.
    """
    try:
        if os.name == 'nt':  # Windows
            # Abre una nueva ventana de cmd, ejecuta el script y la mantiene abierta
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems (Linux, macOS)
            # Abre xterm (o gnome-terminal, konsole, etc. si xterm no está disponible),
            # ejecuta el script y mantiene la ventana abierta.
            # Puedes necesitar instalar xterm: sudo apt-get install xterm
            # O cambiar 'xterm' por 'gnome-terminal -e' o 'konsole -e'
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except FileNotFoundError:
        print("Error: No se encontró el ejecutable de la terminal (cmd/xterm). Asegúrate de que estén en tu PATH.")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

# --- Funciones para la Gestión de Tareas (NUEVAS FUNCIONALIDADES) ---

def cargar_tareas():
    """
    Carga las tareas desde el archivo JSON. Si el archivo no existe, retorna una lista vacía.
    """
    if os.path.exists(TAREAS_FILE):
        try:
            with open(TAREAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo {TAREAS_FILE} está corrupto o vacío. Se creará uno nuevo.")
            return []
    return []

def guardar_tareas(tareas):
    """
    Guarda la lista de tareas en el archivo JSON.
    """
    with open(TAREAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, indent=4) # 'indent=4' para formato legible

def gestionar_tareas_poo():
    """
    Menú y lógica para la gestión de tareas de la materia de Programación Orientada a Objetos.
    Permite añadir, ver y marcar tareas como completadas.
    """
    tareas = cargar_tareas() # Carga las tareas al iniciar la gestión

    while True:
        print("\n--- Mi Dashboard de Tareas de POO ---")
        print("1 - Ver todas mis tareas")
        print("2 - Añadir nueva tarea")
        print("3 - Marcar tarea como completada")
        print("0 - Volver al menú principal")

        opcion_tarea = input("Elige una opción: ")

        if opcion_tarea == '1':
            if not tareas:
                print("\nActualmente no tienes tareas registradas.")
            else:
                print("\n--- Listado de Tareas ---")
                for i, tarea in enumerate(tareas):
                    estado = "[COMPLETADA]" if tarea['completada'] else "[PENDIENTE]"
                    print(f"{i+1}. {estado} {tarea['descripcion']}")
            input("\nPresiona Enter para continuar...") # Pausa para que el usuario pueda leer

        elif opcion_tarea == '2':
            descripcion = input("Describe la nueva tarea (ej. 'Revisar tema de Herencia'): ")
            if descripcion.strip(): # Verifica que la descripción no esté vacía
                tareas.append({"descripcion": descripcion.strip(), "completada": False})
                guardar_tareas(tareas)
                print("Tarea añadida con éxito.")
            else:
                print("La descripción de la tarea no puede estar vacía.")
            input("\nPresiona Enter para continuar...")

        elif opcion_tarea == '3':
            if not tareas:
                print("No hay tareas para marcar como completadas.")
                input("\nPresiona Enter para continuar...")
                continue

            print("\n--- Marcar Tarea como Completada ---")
            for i, tarea in enumerate(tareas):
                estado = "[COMPLETADA]" if tarea['completada'] else "[PENDIENTE]"
                print(f"{i+1}. {estado} {tarea['descripcion']}")

            try:
                num_tarea = int(input("Introduce el número de la tarea a marcar como completada (o 0 para cancelar): ")) - 1
                if num_tarea == -1: # Si el usuario ingresa 0
                    print("Operación cancelada.")
                elif 0 <= num_tarea < len(tareas):
                    if not tareas[num_tarea]['completada']:
                        tareas[num_tarea]['completada'] = True
                        guardar_tareas(tareas)
                        print("Tarea marcada como completada.")
                    else:
                        print("Esta tarea ya estaba completada.")
                else:
                    print("Número de tarea no válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")
            input("\nPresiona Enter para continuar...")

        elif opcion_tarea == '0':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            input("\nPresiona Enter para continuar...")

# --- Menús del Dashboard (MODIFICADOS) ---

def mostrar_menu():
    """
    Muestra el menú principal del Dashboard.
    """
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
        # Puedes añadir más unidades aquí si existen en tu proyecto
    }
    
    # Hemos añadido una nueva opción al menú principal
    opciones_adicionales = {
        'T': 'Gestionar mis Tareas de POO'
    }

    while True:
        print("\n--- Menu Principal del Dashboard POO ---")
        # Imprime las opciones de unidades existentes
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        # Imprime la nueva opción para gestionar tareas
        for key in opciones_adicionales:
            print(f"{key} - {opciones_adicionales[key]}")
        print("0 - Salir")

        eleccion_unidad = input("Elige una opción (número para unidad, 'T' para tareas, '0' para salir): ").upper() # Convertir a mayúsculas para 'T'
        
        if eleccion_unidad == '0':
            print("Saliendo del programa. ¡Hasta pronto!")
            break
        elif eleccion_unidad in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[eleccion_unidad]))
        elif eleccion_unidad == 'T': # Maneja la nueva opción de tareas
            gestionar_tareas_poo()
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
        input("\nPresiona Enter para volver al Menú Principal...")


def mostrar_sub_menu(ruta_unidad):
    """
    Muestra el submenú de subcarpetas dentro de una unidad seleccionada.
    """
    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
    sub_carpetas.sort() # Ordenar alfabéticamente para mejor navegación

    while True:
        print(f"\n--- Submenú de {os.path.basename(ruta_unidad)} ---")
        if not sub_carpetas:
            print("No hay subcarpetas en esta unidad.")
            print("0 - Regresar al menú principal")
        else:
            # Imprime las subcarpetas
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta}")
            print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta_idx = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta_idx < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta_idx]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, ingresa un número.")
        input("\nPresiona Enter para volver al Submenú...")


def mostrar_scripts(ruta_sub_carpeta):
    """
    Muestra los scripts Python dentro de una subcarpeta y permite ver su código o ejecutarlos.
    """
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]
    scripts.sort() # Ordenar alfabéticamente

    while True:
        print(f"\n--- Scripts en {os.path.basename(ruta_sub_carpeta)} ---")
        if not scripts:
            print("No hay scripts Python (.py) en esta carpeta.")
            print("0 - Regresar al submenú anterior")
            print("9 - Regresar al menú principal")
        else:
            # Imprime los scripts
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script}")
            print("0 - Regresar al submenú anterior")
            print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar al submenú, o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return # Esta es la clave para volver al menú principal desde aquí
        else:
            try:
                eleccion_script_idx = int(eleccion_script) - 1
                if 0 <= eleccion_script_idx < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script_idx])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, ingresa un número.")
            input("\nPresiona Enter para volver al menú de scripts.")


# --- Ejecutar el Dashboard ---
if __name__ == "__main__":
    mostrar_menu()
