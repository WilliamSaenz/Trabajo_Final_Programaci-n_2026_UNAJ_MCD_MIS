# estudiantes_csv.py
# MÓDULO 1: LECTURA Y PROCESAMIENTO DE DATOS
# Gestiona el archivo CSV: precarga, lectura, validación e ingreso de alumnos.

import csv #csv: permite leer y escribir archivos
import os #os: se usa para verificar si un archivo existe en la computadora.

# ************************************************************
# REFERENCIAS AUXILIARES
# ************************************************************

ARCHIVO = "estudiantes.csv" #Define el nombre del archivo donde se guardan los estudiantes.

HEADERS = ["Legajo", "Nombre", "Apellido", "Programación", "Análisis Estadístico",  #Define los encabezados del CSV. Son las columnas del archivo: legajo, nombre, apellido y materias.
           "Base de Datos", "Arquitecturas en la Nube",
           "Aprendizaje Automático", "Captura de la Información"]


# ************************************************************
# FUNCIÓN: guardar_estudiantes_csv
# Propósito: Guardar una lista de alumnos en un archivo CSV.
#            Si el archivo no existe, primero escribe los encabezados.
# ************************************************************

def guardar_estudiantes_csv(nombre_archivo, headers, datos): #Esta función guarda alumnos en el archivo CSV.

    archivo_existe = os.path.isfile(nombre_archivo) #Verifica si el archivo ya existe

    with open(nombre_archivo, 'a', newline="", encoding="utf-8") as archivo: #Abre el archivo en modo append, o sea, agrega datos al final sin borrar lo anterior.
        agregar_est = csv.writer(archivo)

        if not archivo_existe:     #Si el archivo no existe, primero escribe los encabezados.
            agregar_est.writerow(headers) 

        agregar_est.writerows(datos) #Guarda una o varias filas de alumnos.


# ************************************************************
# FUNCIÓN: leer_alumnos_csv
# Propósito: Leer un archivo CSV y devolver los encabezados
#            y todas las filas de datos por separado.
# ************************************************************

def leer_alumnos_csv(nombre_archivo): #Esta función lee el archivo CSV y devuelve dos cosas:

    headers = []   # headers: encabezados del archivo.
    datos_rows = []  # datos_rows: filas con alumnos.

    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as lectura:
            reader = csv.reader(lectura)

            try:
                headers = next(reader)
            except StopIteration: #Si el archivo está vacío.
                print("Error: El archivo está vacío.")
                return headers, datos_rows

            datos_rows = list(reader)

    except FileNotFoundError:          #Si el archivo no existe.
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")

    except PermissionError:           #Si no tiene permiso para leerlo.
        print("Ocurrió un error al leer el archivo.")

    return headers, datos_rows 


# ************************************************************
# FUNCIÓN: obtener_legajo
# Propósito: Determina el siguiente número de legajo disponible
#            leyendo el archivo CSV.
# ************************************************************

def obtener_legajo(nombre_archivo):   # Busca cuál es el último legajo usado y devuelve el siguiente.
    headers, datos = leer_alumnos_csv(nombre_archivo) 

    max_legajo = 0

    if datos:
        for alumno_data in datos:
            try:
                legajo_actual = int(alumno_data[0]) #Toma el primer dato de cada fila, que corresponde al legajo.
                if legajo_actual > max_legajo:
                    max_legajo = legajo_actual
            except (ValueError, IndexError):
                print("Advertencia: legajo inválido o no encontrado.")
                continue

    return max_legajo + 1 #Si el mayor legajo era 30, devuelve 31.


# ************************************************************
# FUNCIÓN: pedir_nota
# Propósito: Pedir una nota por teclado y validar que sea
#            un número decimal, entre 1 y 10.
# ************************************************************

def pedir_nota(materia): #Pide una nota y valida que sea numérica y esté entre 1 y 10.

    while True:
        entrada = input(f"Ingrese la nota de {materia}: ")

        try:
            nota = float(entrada) #Pide una nota y valida que sea numérica y esté entre 1 y 10.

            if 1 <= nota <= 10: #Solo acepta notas válidas.
                return nota

            else:
                print("Error: La nota debe estar entre 1 y 10.")

        except ValueError:  #Captura el error si el usuario escribe texto en vez de número.
            print("Error: Debe ingresar un número válido.")


# ************************************************************
# FUNCIÓN: ingresar_alumno
# Propósito: Capturar todos los datos de un alumno por teclado,
#            usando pedir_nota() para validar cada nota.
# ************************************************************

def ingresar_alumno():  # Esta función se encarga de pedir todos los datos de un alumno nuevo.

    legajo = obtener_legajo(ARCHIVO) # Después pide nombre y apellido:

    print(f"\n  --- Ingreso del alumno (Legajo Nro: {legajo}) ---")

    nombre = input("Ingrese el nombre del alumno: ") # Valida que sean solo letras:
    while True:
        if nombre.isalpha(): #isalpha() no acepta espacios y comprobar si todos los caracteres de una cadena de texto (string) son letras
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

# Se piden las notas usando la función pedir_nota():
    programacion = pedir_nota("Programación")
    estadistica = pedir_nota("Análisis Estadístico")
    base_datos = pedir_nota("Base de Datos")
    nube = pedir_nota("Arquitecturas en la Nube")
    aprendizaje = pedir_nota("Aprendizaje Automático")
    captura = pedir_nota("Captura de la Información")

    return [str(legajo), nombre, apellido, programacion,  # devuelve una lista con todos los datos del alumno
            estadistica, base_datos, nube, aprendizaje,
            captura]


# ************************************************************
# FUNCIÓN: precargar_datos
# Propósito: Si el archivo CSV no existe, crearlo con alumnos
#            de ejemplo para no arrancar siempre desde cero.
# ************************************************************

def precargar_datos(nombre_archivo, headers):  # Esta función crea el archivo con 30 alumnos de ejemplo si todavía no existe

    if not os.path.isfile(nombre_archivo): # Si el archivo no existe, carga los datos iniciales.

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

        guardar_estudiantes_csv(nombre_archivo, headers, datos_iniciales) #Usa la función anterior para guardar esos alumnos; esto permite que el sistema no empiece desde cero.
        print(f"Archivo '{nombre_archivo}' creado con {len(datos_iniciales)} alumnos precargados.\n")

    else:
        print(f"Archivo '{nombre_archivo}' encontrado con datos existentes.\n")


# ************************************************************
# FUNCIÓN: ejecutar_modulo1
# Propósito: Punto de entrada del módulo. Precarga datos y
#            permite ingresar alumnos nuevos por teclado.
# ************************************************************

def ejecutar_modulo1():  # Es la función principal del módulo.

    precargar_datos(ARCHIVO, HEADERS) # Primer acción: precarga datos:

    print("*" * 50)
    print("  --- Sistema de ingreso de alumnos ---")
    print("*" * 50)

    while True:

        while True: #Segundo acción: permite ingresar alumnos nuevos:
            agregar = input("\n¿Desea ingresar un nuevo alumno? (s/n): ").lower() #Valida que el usuario escriba solo s o n.

            if agregar != 's' and agregar != 'n':
                print("Error: Debe ingresar 's' o 'n'.")
            else:
                break

        if agregar != 's':
            break
# Si responde "s", llama a:
        alumno = ingresar_alumno()
        guardar_estudiantes_csv(ARCHIVO, HEADERS, [alumno])
        print("Alumno guardado correctamente.\n")

    print("\n--- Alumnos registrados ---")
# Al final muestra todos los alumnos registrados:
    headers, datos = leer_alumnos_csv(ARCHIVO)

    if headers:
        print(" | ".join(headers))
        print("-" * 100)
        for fila in datos:
            print(" | ".join(str(v) for v in fila))

    print(f"\nTotal de alumnos: {len(datos)}")

#Bloque final: Si este archivo se ejecuta directamente, correr el programa principal; Pero si este archivo se importa desde otro módulo, no ejecutar automáticamente.
if __name__ == "__main__":
    ejecutar_modulo1()
