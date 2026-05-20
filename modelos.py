# modelos.py
# MÓDULO 2: MODELADO ORIENTADO A OBJETOS Y ANÁLISIS ACADÉMICO
# Clases Estudiante y Curso para representar y analizar datos académicos.

import pandas as pd

# ************************************************************
# CLASE ESTUDIANTE
# Propósito: Representar a un alumno con sus datos personales,
# calificaciones y métodos de análisis individual.
# ************************************************************

class Estudiante:

    # ************************************************************
    # REFERENCIAS AUXILIARES
    # ************************************************************
    ASIGNATURAS = [
        "Programación",
        "Análisis Estadístico",
        "Base de Datos",
        "Arquitecturas en la Nube",
        "Aprendizaje Automático",
        "Captura de la Información",
    ]

    NOTA_APROBACION = 6.0   # >= 6 aprueba
    NOTA_APLAZO = 4.0       # < 4 es aplazo

    # Definición de atributos
    def __init__(self, legajo, nombre, apellido, notas):
        self.__legajo   = int(legajo)
        self.__nombre   = str(nombre).strip()
        self.__apellido = str(apellido).strip()
        self.__notas    = notas  # dict: {"Programación": 8.0, ...}

    # --- Getters ---

    def getLegajo(self):
        return self.__legajo

    def getNombre(self):
        return self.__nombre

    def getApellido(self):
        return self.__apellido

    def getNotas(self):
        return self.__notas

    def getNombreCompleto(self):
        return f"{self.__nombre} {self.__apellido}"

    # --- Setters ---

    def setNombre(self, nombre_nuevo):
        self.__nombre = nombre_nuevo

    def setApellido(self, apellido_nuevo):
        self.__apellido = apellido_nuevo

    # --- Métodos de análisis ---

    def clasificar_nota(self, nota):
        if nota >= 6:
            return "Aprobado"
        elif nota >= 4:
            return "Desaprobado"
        else:
            return "Aplazo"

    def calcular_promedio(self):
        valores = list(self.__notas.values())
        if len(valores) == 0:
            return 0.0
        return round(sum(valores) / len(valores), 2)

    def calcular_promedio_sin_aplazos(self):
        notas_validas = []
        for n in self.__notas.values():
            if n >= self.NOTA_APLAZO:
                notas_validas.append(n)

        if len(notas_validas) == 0:
            return 0.0
        return round(sum(notas_validas) / len(notas_validas), 2)

    def obtener_situacion(self):
        for nota in self.__notas.values():
            if nota < self.NOTA_APROBACION:
                return "Reprobado"
        return "Aprobado"

    def contar_aprobadas(self):
        contador = 0
        for n in self.__notas.values():
            if n >= self.NOTA_APROBACION:
                contador += 1
        return contador

    def contar_desaprobados(self):
        contador = 0
        for n in self.__notas.values():
            if self.NOTA_APLAZO <= n < self.NOTA_APROBACION:
                contador += 1
        return contador

    def contar_aplazos(self):
        contador = 0
        for n in self.__notas.values():
            if n < self.NOTA_APLAZO:
                contador += 1
        return contador

    def materias_reprobadas(self):
        reprobadas = []
        for materia, nota in self.__notas.items():
            if nota < self.NOTA_APROBACION:
                reprobadas.append(materia)
        return reprobadas

    def resumen_est(self):
        resumen = {
            "Legajo":   self.__legajo,
            "Nombre":   self.__nombre,
            "Apellido": self.__apellido,
        }
        for materia, nota in self.__notas.items():
            resumen[materia] = nota

        resumen["Promedio"] = self.calcular_promedio()
        resumen["Prom. sin aplazos"] = self.calcular_promedio_sin_aplazos()
        resumen["Situación"] = self.obtener_situacion()
        return resumen

    def mostrar(self):
        print(f"[{self.__legajo:>3}] {self.__nombre} {self.__apellido:<20} "
              f"Prom: {self.calcular_promedio():.2f}  —  {self.obtener_situacion()}")


# ************************************************************
# CLASE CURSO
# Propósito: Agrupar estudiantes cargados desde CSV y realizar
# análisis estadístico grupal.
# ************************************************************

class Curso:

    def __init__(self, nombre_archivo):
        self.__nombre_archivo = nombre_archivo
        self.__estudiantes = []
        self.__cargar_desde_csv()

    # --- Getters ---

    def getEstudiantes(self):
        return self.__estudiantes

    def getCantidad(self):
        return len(self.__estudiantes)

    # --- Carga de datos ---

    def __cargar_desde_csv(self):
        try:
            df = pd.read_csv(self.__nombre_archivo)
        except FileNotFoundError:
            print(f"Error: no se encontró el archivo '{self.__nombre_archivo}'.")
            return

        for i in range(len(df)):
            fila = df.iloc[i]
            notas = {}
            for materia in Estudiante.ASIGNATURAS:
                notas[materia] = float(fila[materia])

            alumno = Estudiante(fila["Legajo"], fila["Nombre"], fila["Apellido"], notas)
            self.__estudiantes.append(alumno)

        print(f"Se cargaron {len(self.__estudiantes)} estudiantes desde '{self.__nombre_archivo}'.")

    def recargar(self):
        self.__estudiantes = []
        self.__cargar_desde_csv()

    # --- Métodos de búsqueda ---

    def buscar_por_legajo(self, legajo):
        for est in self.__estudiantes:
            if est.getLegajo() == legajo:
                return est
        return None

    # --- Métodos de análisis grupal ---

    def promedio_por_asignatura(self):
        resultado = {}
        for materia in Estudiante.ASIGNATURAS:
            suma = 0
            for est in self.__estudiantes:
                suma += est.getNotas()[materia]
            resultado[materia] = round(suma / len(self.__estudiantes), 2)
        return resultado

    def porcentaje_aprobacion(self):
        if len(self.__estudiantes) == 0:
            return 0.0
        aprobados = 0
        for est in self.__estudiantes:
            if est.obtener_situacion() == "Aprobado":
                aprobados += 1
        return round((aprobados / len(self.__estudiantes)) * 100, 1)

    def porcentaje_aprobacion_por_asignatura(self):
        resultado = {}
        total = len(self.__estudiantes)
        for materia in Estudiante.ASIGNATURAS:
            aprobados = 0
            for est in self.__estudiantes:
                if est.getNotas()[materia] >= 6:
                    aprobados += 1
            resultado[materia] = round((aprobados / total) * 100, 1)
        return resultado

    def asignatura_mayor_rendimiento(self):
        promedios = self.promedio_por_asignatura()
        mejor = None
        mejor_prom = 0
        for materia, prom in promedios.items():
            if mejor is None or prom > mejor_prom:
                mejor = materia
                mejor_prom = prom
        return mejor, mejor_prom

    def asignatura_menor_rendimiento(self):
        promedios = self.promedio_por_asignatura()
        peor = None
        peor_prom = 11
        for materia, prom in promedios.items():
            if peor is None or prom < peor_prom:
                peor = materia
                peor_prom = prom
        return peor, peor_prom

    def mejor_estudiante(self):
        if len(self.__estudiantes) == 0:
            return None
        mejor = self.__estudiantes[0]
        for est in self.__estudiantes:
            if est.calcular_promedio() > mejor.calcular_promedio():
                mejor = est
        return mejor

    def estudiantes_reprobados(self):
        reprobados = []
        for est in self.__estudiantes:
            if est.obtener_situacion() == "Reprobado":
                reprobados.append(est)
        return reprobados

    def to_dataframe(self):
        lista_dicts = []
        for est in self.__estudiantes:
            lista_dicts.append(est.resumen_est())
        return pd.DataFrame(lista_dicts)

    def mostrar(self):
        print(f"Curso ({len(self.__estudiantes)} estudiantes):")
        print("-" * 65)
        for est in self.__estudiantes:
            est.mostrar()


# ************************************************************
# EJECUCIÓN DE PRUEBA (si se ejecuta directamente)
# ************************************************************

if __name__ == "__main__":

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
