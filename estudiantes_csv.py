# estudiantes_csv.py
# MÓDULO 1: LECTURA Y PROCESAMIENTO DE DATOS
# Gestiona el archivo CSV: precarga, lectura, validación e ingreso de alumnos.

import csv
import os

# ************************************************************
# REFERENCIAS AUXILIARES
# ************************************************************

ARCHIVO = "estudiantes.csv"

HEADERS = ["Legajo", "Nombre", "Apellido", "Programación", "Análisis Estadístico",
           "Base de Datos", "Arquitecturas en la Nube",
           "Aprendizaje Automático", "Captura de la Información"]


# ************************************************************
# FUNCIÓN: guardar_estudiantes_csv
# Propósito: Guardar una lista de alumnos en un archivo CSV.
#            Si el archivo no existe, primero escribe los encabezados.
# ************************************************************

def guardar_estudiantes_csv(nombre_archivo, headers, datos):

    archivo_existe = os.path.isfile(nombre_archivo)

    with open(nombre_archivo, 'a', newline="", encoding="utf-8") as archivo:
        agregar_est = csv.writer(archivo)

        if not archivo_existe:
            agregar_est.writerow(headers)

        agregar_est.writerows(datos)


# ************************************************************
# FUNCIÓN: leer_alumnos_csv
# Propósito: Leer un archivo CSV y devolver los encabezados
#            y todas las filas de datos por separado.
# ************************************************************

def leer_alumnos_csv(nombre_archivo):

    headers = []
    datos_rows = []

    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as lectura:
            reader = csv.reader(lectura)

            try:
                headers = next(reader)
            except StopIteration:
                print("Error: El archivo está vacío.")
                return headers, datos_rows

            datos_rows = list(reader)

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")

    except PermissionError:
        print("Ocurrió un error al leer el archivo.")

    return headers, datos_rows


# ************************************************************
# FUNCIÓN: obtener_legajo
# Propósito: Determina el siguiente número de legajo disponible
#            leyendo el archivo CSV.
# ************************************************************

def obtener_legajo(nombre_archivo):
    headers, datos = leer_alumnos_csv(nombre_archivo)

    max_legajo = 0

    if datos:
        for alumno_data in datos:
            try:
                legajo_actual = int(alumno_data[0])
                if legajo_actual > max_legajo:
                    max_legajo = legajo_actual
            except (ValueError, IndexError):
                print("Advertencia: legajo inválido o no encontrado.")
                continue

    return max_legajo + 1


# ************************************************************
# FUNCIÓN: pedir_nota
# Propósito: Pedir una nota por teclado y validar que sea
#            un número decimal, entre 1 y 10.
# ************************************************************

def pedir_nota(materia):

    while True:
        entrada = input(f"Ingrese la nota de {materia}: ")

        try:
            nota = float(entrada)

            if 1 <= nota <= 10:
                return nota

            else:
                print("Error: La nota debe estar entre 1 y 10.")

        except ValueError:
            print("Error: Debe ingresar un número válido.")


# ************************************************************
# FUNCIÓN: ingresar_alumno
# Propósito: Capturar todos los datos de un alumno por teclado,
#            usando pedir_nota() para validar cada nota.
# ************************************************************

def ingresar_alumno():

    legajo = obtener_legajo(ARCHIVO)

    print(f"\n  --- Ingreso del alumno (Legajo Nro: {legajo}) ---")

    nombre = input("Ingrese el nombre del alumno: ")
    while True:
        if nombre.isalpha():
            break
        else:
            print("Error: El nombre debe contener solo letras.")
            nombre = input("Ingrese el nombre del alumno: ")

    apellido = input("Ingrese el apellido del alumno: ")
    while True:
        if apellido.isalpha():
            break
        else:
            print("Error: El apellido debe contener solo letras.")
            apellido = input("Ingrese el apellido del alumno: ")

    programacion = pedir_nota("Programación")
    estadistica = pedir_nota("Análisis Estadístico")
    base_datos = pedir_nota("Base de Datos")
    nube = pedir_nota("Arquitecturas en la Nube")
    aprendizaje = pedir_nota("Aprendizaje Automático")
    captura = pedir_nota("Captura de la Información")

    return [str(legajo), nombre, apellido, programacion,
            estadistica, base_datos, nube, aprendizaje,
            captura]


# ************************************************************
# FUNCIÓN: precargar_datos
# Propósito: Si el archivo CSV no existe, crearlo con alumnos
#            de ejemplo para no arrancar siempre desde cero.
# ************************************************************

def precargar_datos(nombre_archivo, headers):

    if not os.path.isfile(nombre_archivo):

        datos_iniciales = [
            ["1",  "Juan",      "Pérez",      8.0, 7.5, 9.0, 6.0, 8.0, 7.0],
            ["2",  "María",     "González",    9.0, 8.5, 7.0, 9.0, 10.0, 8.0],
            ["3",  "Carlos",    "López",       6.0, 7.0, 8.0, 7.0, 6.0, 9.0],
            ["4",  "Ana",       "Martínez",   10.0, 9.0, 8.5, 8.0, 9.0, 10.0],
            ["5",  "Luis",      "Rodríguez",   7.0, 4.5, 7.0, 8.0, 5.0, 6.0],
            ["6",  "Sofía",     "Ramírez",     9.0, 10.0, 9.0, 8.0, 7.0, 8.0],
            ["7",  "Martín",    "Herrera",     2.0, 3.0, 4.0, 1.0, 5.0, 3.0],
            ["8",  "Valentina", "Castro",      8.0, 7.0, 8.0, 9.0, 6.0, 7.0],
            ["9",  "Nicolás",   "Moreno",      6.0, 6.0, 5.0, 7.0, 4.0, 6.0],
            ["10", "Camila",    "Ruiz",        7.0, 8.0, 9.0, 6.0, 8.0, 5.0],
            ["11", "Federico",  "Álvarez",     4.0, 5.0, 3.0, 6.0, 2.0, 7.0],
            ["12", "Laura",     "Méndez",     10.0, 8.0, 9.0, 7.0, 9.0, 10.0],
            ["13", "Agustín",   "Romero",      7.0, 6.0, 8.0, 5.0, 7.0, 6.0],
            ["14", "Florencia", "Gómez",       9.0, 8.0, 7.0, 8.0, 9.0, 8.0],
            ["15", "Ramiro",    "Acosta",      3.0, 2.0, 4.0, 3.0, 5.0, 4.0],
            ["16", "Julieta",   "Peralta",     8.0, 9.0, 7.0, 6.0, 8.0, 9.0],
            ["17", "Sebastián", "Molina",      5.0, 4.0, 6.0, 7.0, 3.0, 5.0],
            ["18", "Daniela",   "Ríos",       10.0, 10.0, 9.0, 8.0, 10.0, 9.0],
            ["19", "Tomás",     "Vega",        6.0, 7.0, 5.0, 4.0, 6.0, 7.0],
            ["20", "Milagros",  "Silva",       7.0, 6.0, 8.0, 7.0, 5.0, 6.0],
            ["21", "Emilio",    "Paz",         4.0, 5.0, 3.0, 2.0, 4.0, 6.0],
            ["22", "Rocío",     "Luna",        8.0, 9.0, 8.0, 7.0, 7.0, 8.0],
            ["23", "Ignacio",   "Cabrera",     6.0, 5.0, 7.0, 6.0, 8.0, 5.0],
            ["24", "Abril",     "Suárez",      9.0, 8.0, 10.0, 7.0, 9.0, 8.0],
            ["25", "Gonzalo",   "Medina",      3.0, 4.0, 5.0, 3.0, 2.0, 4.0],
            ["26", "Carolina",  "Bustos",      7.0, 7.0, 6.0, 8.0, 7.0, 6.0],
            ["27", "Leandro",   "Figueroa",    5.0, 6.0, 4.0, 5.0, 6.0, 3.0],
            ["28", "Elena",     "Martínez",    9.0, 9.0, 8.0, 2.0, 6.0, 7.0],
            ["29", "Pedro",     "Sánchez",     3.0, 4.0, 2.0, 5.0, 3.0, 6.0],
            ["30", "Lucía",     "Díaz",        7.0, 8.0, 6.0, 7.0, 8.0, 7.0],
        ]

        guardar_estudiantes_csv(nombre_archivo, headers, datos_iniciales)
        print(f"Archivo '{nombre_archivo}' creado con {len(datos_iniciales)} alumnos precargados.\n")

    else:
        print(f"Archivo '{nombre_archivo}' encontrado con datos existentes.\n")


# ************************************************************
# FUNCIÓN: ejecutar_modulo1
# Propósito: Punto de entrada del módulo. Precarga datos y
#            permite ingresar alumnos nuevos por teclado.
# ************************************************************

def ejecutar_modulo1():

    precargar_datos(ARCHIVO, HEADERS)

    print("*" * 50)
    print("  --- Sistema de ingreso de alumnos ---")
    print("*" * 50)

    while True:

        while True:
            agregar = input("\n¿Desea ingresar un nuevo alumno? (s/n): ").lower()

            if agregar != 's' and agregar != 'n':
                print("Error: Debe ingresar 's' o 'n'.")
            else:
                break

        if agregar != 's':
            break

        alumno = ingresar_alumno()
        guardar_estudiantes_csv(ARCHIVO, HEADERS, [alumno])
        print("Alumno guardado correctamente.\n")

    print("\n--- Alumnos registrados ---")

    headers, datos = leer_alumnos_csv(ARCHIVO)

    if headers:
        print(" | ".join(headers))
        print("-" * 100)
        for fila in datos:
            print(" | ".join(str(v) for v in fila))

    print(f"\nTotal de alumnos: {len(datos)}")


# Si se ejecuta directamente
if __name__ == "__main__":
    ejecutar_modulo1()
