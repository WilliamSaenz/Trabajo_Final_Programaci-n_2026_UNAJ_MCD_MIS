# modelos.py
# MÓDULO 2: MODELADO ORIENTADO A OBJETOS Y ANÁLISIS ACADÉMICO
# Clases Estudiante y Curso para representar y analizar datos académicos.

import pandas as pd # Se utiliza pandas para leer el archivo CSV y convertirlo en una tabla de datos.

# ************************************************************
# CLASE ESTUDIANTE
# Propósito: Representar a un alumno con sus datos personales,
# calificaciones y métodos de análisis individual.
# ************************************************************

class Estudiante: #Representa a un alumno individual, con su legajo, nombre, apellido y notas.

    # ************************************************************
    # REFERENCIAS AUXILIARES
    # ************************************************************
    # Variables de clase: Lista las materias que tiene cada alumno.
    ASIGNATURAS = [
        "Programación",
        "Análisis Estadístico",
        "Base de Datos",
        "Arquitecturas en la Nube",
        "Aprendizaje Automático",
        "Captura de la Información",
    ]
# Define dos criterios:
    NOTA_APROBACION = 6.0   # >= 6 aprueba
    NOTA_APLAZO = 4.0       # < 4 es aplazo

    # Definición de atributos
    def __init__(self, legajo, nombre, apellido, notas): # Constructor: Este método se ejecuta cuando se crea un estudiante.
        self.__legajo   = int(legajo)   # Guarda los datos del alumno; El doble guion bajo __ indica que son atributos privados: No debería tocarse directamente desde afuera de la clase. Para acceder se usan los getters.
        self.__nombre   = str(nombre).strip()
        self.__apellido = str(apellido).strip()
        self.__notas    = notas  # dict: {"Programación": 8.0, ...}

    # --- Getters ---

    def getLegajo(self):   #Los getters permiten consultar datos privados.
        return self.__legajo

    def getNombre(self):
        return self.__nombre

    def getApellido(self):
        return self.__apellido

    def getNotas(self):
        return self.__notas

    def getNombreCompleto(self):
        return f"{self.__nombre} {self.__apellido}" #Acá se estructura el nombre completo.

    # --- Setters ---

    def setNombre(self, nombre_nuevo):   #  Permiten modificar datos: nombre y apellido; No se modifica el legajo, lo cual tiene sentido porque el legajo debería ser único y estable.
        self.__nombre = nombre_nuevo

    def setApellido(self, apellido_nuevo):
        self.__apellido = apellido_nuevo

    # --- Métodos de análisis ---

    def clasificar_nota(self, nota):
        #Clasifica una nota individual:
        if nota >= 6:
            return "Aprobado"
        elif nota >= 4:
            return "Desaprobado"
        else:
            return "Aplazo"

    def calcular_promedio(self):  # Calcula el promedio de todas las materias.
        valores = list(self.__notas.values()) # Convierte las notas del diccionario en una lista.
        if len(valores) == 0:
            return 0.0
        return round(sum(valores) / len(valores), 2) # Suma todas las notas, divide por la cantidad y redondea a 2 decimales.

    def calcular_promedio_sin_aplazos(self):  # Calcula el promedio, pero excluye las notas menores a 4.
        notas_validas = []
        for n in self.__notas.values():
            # Solo toma notas desde 4 en adelante. Esto permite comparar el rendimiento sin que los aplazos bajen tanto el promedio.
            if n >= self.NOTA_APLAZO:
                notas_validas.append(n)

        if len(notas_validas) == 0:
            return 0.0
        return round(sum(notas_validas) / len(notas_validas), 2)

    def obtener_situacion(self):  # Determina si el estudiante aprueba o reprueba el conjunto de materias.
        for nota in self.__notas.values():
            if nota < self.NOTA_APROBACION:
                return "Reprobado"
        return "Aprobado"
        # Si tiene una sola materia menor a 6, queda como “Reprobado”.

    def contar_aprobadas(self): # Cuenta notas mayores o iguales a 6.
        contador = 0
        for n in self.__notas.values():
            if n >= self.NOTA_APROBACION:
                contador += 1
        return contador

    def contar_desaprobados(self): # Cuenta notas entre 4 y menos de 6.
        contador = 0
        for n in self.__notas.values():
            if self.NOTA_APLAZO <= n < self.NOTA_APROBACION:
                contador += 1
        return contador

    def contar_aplazos(self): # Cuenta notas menores a 4.
        contador = 0
        for n in self.__notas.values():
            if n < self.NOTA_APLAZO:
                contador += 1
        return contador

    def materias_reprobadas(self): # Devuelve una lista con las materias donde el alumno tiene nota menor a 6.
        reprobadas = []
        for materia, nota in self.__notas.items():
            if nota < self.NOTA_APROBACION:
                reprobadas.append(materia)
        return reprobadas

    def resumen_est(self): # Arma un diccionario con toda la información del estudiante:
        resumen = {
            "Legajo":   self.__legajo,
            "Nombre":   self.__nombre,
            "Apellido": self.__apellido,
        }
        for materia, nota in self.__notas.items():
            resumen[materia] = nota
# Luego agrega las notas de cada materia y finalmente: Esto sirve mucho porque después se puede convertir en un DataFrame de pandas.
        resumen["Promedio"] = self.calcular_promedio()
        resumen["Prom. sin aplazos"] = self.calcular_promedio_sin_aplazos()
        resumen["Situación"] = self.obtener_situacion()
        return resumen

    def mostrar(self): #Imprime en pantalla un resumen breve del alumno:
        print(f"[{self.__legajo:>3}] {self.__nombre} {self.__apellido:<20} "
              f"Prom: {self.calcular_promedio():.2f}  —  {self.obtener_situacion()}")


# ************************************************************
# CLASE CURSO
# Propósito: Agrupar estudiantes cargados desde CSV y realizar
# análisis estadístico grupal.
# ************************************************************

class Curso: # Representa al grupo completo de estudiantes, cargado desde el archivo CSV.

    def __init__(self, nombre_archivo):  # Cuando se crea un curso, recibe el nombre del archivo CSV. 
                                            # Hace tres cosas: 1.Guarda el nombre del archivo, 2.Crea una lista vacía de estudiantes, 3. Carga automáticamente los estudiantes desde el CSV
        self.__nombre_archivo = nombre_archivo
        self.__estudiantes = []
        self.__cargar_desde_csv()

    # --- Getters ---

    def getEstudiantes(self):
        return self.__estudiantes

    def getCantidad(self):
        return len(self.__estudiantes)

    # --- Carga de datos ---

    def __cargar_desde_csv(self):  # Carga desde CSV 
        try:
            df = pd.read_csv(self.__nombre_archivo) # Este método lee el archivo
        except FileNotFoundError:
            print(f"Error: no se encontró el archivo '{self.__nombre_archivo}'.")
            return

        for i in range(len(df)):   # Después recorre cada fila
            fila = df.iloc[i]
            notas = {} # Arma un diccionario de notas
            for materia in Estudiante.ASIGNATURAS:
                notas[materia] = float(fila[materia])
            # Crea un objeto Estudiante:
            alumno = Estudiante(fila["Legajo"], fila["Nombre"], fila["Apellido"], notas)
            self.__estudiantes.append(alumno) # Finalmente lo agrega a la lista del curso

        print(f"Se cargaron {len(self.__estudiantes)} estudiantes desde '{self.__nombre_archivo}'.")

    def recargar(self):   # Sirve para Vacíar la lista y volver a leer el CSV; Sirve si el archivo fue actualizado y precisa refrescar los datos sin cerrar el programa.
        self.__estudiantes = []
        self.__cargar_desde_csv()

    # --- Métodos de búsqueda ---

    def buscar_por_legajo(self, legajo): # Recorre todos los estudiantes y devuelve el que tenga ese legajo.
        for est in self.__estudiantes:
            if est.getLegajo() == legajo:
                return est
        return None

    # --- Métodos de análisis grupal ---

    def promedio_por_asignatura(self): #Calcula el promedio de cada materia en todo el curso.
        resultado = {}
        for materia in Estudiante.ASIGNATURAS:
            suma = 0
            for est in self.__estudiantes:
                suma += est.getNotas()[materia]
            resultado[materia] = round(suma / len(self.__estudiantes), 2)
        return resultado

    def porcentaje_aprobacion(self):  # Calcula qué porcentaje de estudiantes aprobaron todas las materias.
        if len(self.__estudiantes) == 0:
            return 0.0
        aprobados = 0
        for est in self.__estudiantes:
            if est.obtener_situacion() == "Aprobado":
                aprobados += 1
        return round((aprobados / len(self.__estudiantes)) * 100, 1)

    def porcentaje_aprobacion_por_asignatura(self): # Calcula el porcentaje de aprobados en cada materia.
        resultado = {}
        total = len(self.__estudiantes)
        for materia in Estudiante.ASIGNATURAS:
            aprobados = 0
            for est in self.__estudiantes:
                # Esto permite saber qué materia tuvo mejor o peor rendimiento.
                if est.getNotas()[materia] >= 6:
                    aprobados += 1
            resultado[materia] = round((aprobados / total) * 100, 1)
        return resultado

    def asignatura_mayor_rendimiento(self): # Busca la materia con promedio más alto.
        promedios = self.promedio_por_asignatura()
        mejor = None
        mejor_prom = 0
        for materia, prom in promedios.items():
            if mejor is None or prom > mejor_prom:
                mejor = materia
                mejor_prom = prom
        return mejor, mejor_prom

    def asignatura_menor_rendimiento(self): # Busca la materia con promedio más bajo.
        promedios = self.promedio_por_asignatura()
        peor = None
        peor_prom = 11
        for materia, prom in promedios.items():
            if peor is None or prom < peor_prom:
                peor = materia
                peor_prom = prom
        return peor, peor_prom

    def mejor_estudiante(self):  # Busca el alumno con mayor promedio general.
        if len(self.__estudiantes) == 0:
            return None
        mejor = self.__estudiantes[0]
        for est in self.__estudiantes:
            # Devuelve el objeto completo del estudiante, no solo el nombre.
            if est.calcular_promedio() > mejor.calcular_promedio():
                mejor = est
        return mejor

    def estudiantes_reprobados(self): #Devuelve una lista con todos los estudiantes cuya situación sea “Reprobado”.
        reprobados = []
        for est in self.__estudiantes:
            if est.obtener_situacion() == "Reprobado":
                reprobados.append(est)
        return reprobados

    def to_dataframe(self): # Convierte todos los estudiantes a una tabla de pandas.
        lista_dicts = []
        for est in self.__estudiantes:
            lista_dicts.append(est.resumen_est())
        return pd.DataFrame(lista_dicts) # Esto es muy útil para después hacer gráficos, estadísticas o exportar resultados.

    def mostrar(self): # Imprime todos los estudiantes cargados en consola.
        print(f"Curso ({len(self.__estudiantes)} estudiantes):")
        print("-" * 65)
        for est in self.__estudiantes:
            est.mostrar()


# ************************************************************
# EJECUCIÓN DE PRUEBA (si se ejecuta directamente)
# ************************************************************

if __name__ == "__main__": #Ojo: Este bloque se ejecuta solo si se ejecuta directamente modelos.py.

    ARCHIVO = "estudiantes.csv"
    curso = Curso(ARCHIVO)

    curso.mostrar()

    print("\nPromedio por asignatura:")
    for materia, prom in curso.promedio_por_asignatura().items():
        print(f"  {materia:<35} {prom:.2f}")

    print(f"\nAprobación general: {curso.porcentaje_aprobacion()}%")

    mejor_asig, prom_mejor = curso.asignatura_mayor_rendimiento()
    peor_asig, prom_peor = curso.asignatura_menor_rendimiento()

    print(f"Mejor asignatura : {mejor_asig} ({prom_mejor})")
    print(f"Peor asignatura  : {peor_asig} ({prom_peor})")
