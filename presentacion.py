# presentacion.py
# MÓDULO 3: PRESENTACIÓN DE RESULTADOS
# Menú interactivo con reportes por consola y gráficos con matplotlib.

import matplotlib.pyplot as plt
from modelos import Estudiante, Curso

ARCHIVO = "estudiantes.csv"


# ************************************************************
# FUNCIONES AUXILIARES
# ************************************************************

def separador(titulo=""):
    print("\n" + "=" * 65)
    if titulo:
        print(f"  {titulo}")
        print("=" * 65)


def pausa():
    import time
    print("\n  Volviendo al menú en 3 segundos...")
    time.sleep(3)


# ************************************************************
# OPCIÓN 1: LISTADO COMPLETO
# ************************************************************

def opcion_listado(curso):
    separador("LISTADO COMPLETO DE ESTUDIANTES")
    for est in curso.getEstudiantes():
        est.mostrar()
    print(f"\n  Total: {curso.getCantidad()} estudiantes")
    pausa()


# ************************************************************
# OPCIÓN 2: BUSCAR POR LEGAJO
# ************************************************************

def opcion_buscar_legajo(curso):
    separador("BUSCAR ESTUDIANTE POR LEGAJO")
    try:
        legajo = int(input("  Ingrese el número de legajo: "))
    except ValueError:
        print("  Error: Debe ingresar un número entero.")
        pausa()
        return

    est = curso.buscar_por_legajo(legajo)

    if est is None:
        print(f"  No se encontró un estudiante con legajo #{legajo}.")
    else:
        print(f"\n  Estudiante: {est.getNombreCompleto()} (Legajo #{est.getLegajo()})")
        print(f"  {'─' * 50}")

        for materia, nota in est.getNotas().items():
            clasif = est.clasificar_nota(nota)
            print(f"    {materia:<30s} : {nota:>5.1f}  {clasif}")

        print(f"  {'─' * 50}")
        print(f"    Promedio (con aplazos)  : {est.calcular_promedio():.2f}")
        print(f"    Promedio (sin aplazos)  : {est.calcular_promedio_sin_aplazos():.2f}")
        print(f"    Aprobadas               : {est.contar_aprobadas()} / 6")
        print(f"    Desaprobados            : {est.contar_desaprobados()}")
        print(f"    Aplazos                 : {est.contar_aplazos()}")
        print(f"    Situación académica     : {est.obtener_situacion()}")

        if len(est.materias_reprobadas()) > 0:
            print(f"    Materias a recuperar    : {', '.join(est.materias_reprobadas())}")

    pausa()


# ************************************************************
# OPCIÓN 3: PROMEDIO INDIVIDUAL
# ************************************************************

def opcion_promedio_individual(curso):
    separador("PROMEDIO INDIVIDUAL POR ESTUDIANTE")

    print(f"  {'Legajo':<8} {'Nombre':<25} {'Prom.':<8} {'Sin apl.':<10} {'Situación'}")
    print(f"  {'-'*8} {'-'*25} {'-'*8} {'-'*10} {'-'*12}")

    for est in curso.getEstudiantes():
        print(f"  {est.getLegajo():<8} {est.getNombreCompleto():<25} "
              f"{est.calcular_promedio():<8.2f} "
              f"{est.calcular_promedio_sin_aplazos():<10.2f} "
              f"{est.obtener_situacion()}")

    pausa()


# ************************************************************
# OPCIÓN 4: ESTADÍSTICAS GENERALES
# ************************************************************

def opcion_promedio_general(curso):
    separador("ESTADÍSTICAS GENERALES DEL CURSO")

    total = curso.getCantidad()
    reprobados = len(curso.estudiantes_reprobados())
    aprobados = total - reprobados

    mejor = curso.mejor_estudiante()
    mejor_asig, prom_mejor = curso.asignatura_mayor_rendimiento()
    peor_asig, prom_peor = curso.asignatura_menor_rendimiento()

    suma_promedios = 0
    for est in curso.getEstudiantes():
        suma_promedios += est.calcular_promedio()
    prom_general = suma_promedios / total

    print(f"    Total de estudiantes    : {total}")
    print(f"    Aprobados               : {aprobados} ({curso.porcentaje_aprobacion()}%)")
    print(f"    Reprobados              : {reprobados} ({100 - curso.porcentaje_aprobacion()}%)")
    print(f"    Promedio general        : {prom_general:.2f}")
    print(f"    Mejor estudiante        : {mejor.getNombreCompleto()} ({mejor.calcular_promedio():.2f})")
    print(f"    Mejor asignatura        : {mejor_asig} ({prom_mejor})")
    print(f"    Peor asignatura         : {peor_asig} ({prom_peor})")

    pausa()


# ************************************************************
# OPCIÓN 5: PROMEDIO POR ASIGNATURA
# ************************************************************

def opcion_promedio_asignatura(curso):
    separador("PROMEDIO POR ASIGNATURA")

    promedios = curso.promedio_por_asignatura()
    aprobacion = curso.porcentaje_aprobacion_por_asignatura()

    print(f"  {'Asignatura':<35} {'Promedio':<10} {'% Aprob.'}")
    print(f"  {'-'*35} {'-'*10} {'-'*10}")

    for materia in Estudiante.ASIGNATURAS:
        print(f"  {materia:<35} {promedios[materia]:<10.2f} {aprobacion[materia]:>6.1f}%")

    pausa()


# ************************************************************
# OPCIÓN 6: DETALLE POR MATERIA
# ************************************************************

def opcion_detalle_materia(curso):
    separador("DETALLE POR MATERIA")

    print("  Materias disponibles:")
    for i in range(len(Estudiante.ASIGNATURAS)):
        print(f"    {i + 1}. {Estudiante.ASIGNATURAS[i]}")

    try:
        opcion = int(input("\n  Seleccione una materia (1-6): "))
        if opcion < 1 or opcion > 6:
            print("  Error: Opción fuera de rango.")
            pausa()
            return
    except ValueError:
        print("  Error: Debe ingresar un número.")
        pausa()
        return

    materia = Estudiante.ASIGNATURAS[opcion - 1]
    separador(f"DETALLE: {materia.upper()}")

    # Ordenar por nota (burbuja)
    lista = list(curso.getEstudiantes())
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[j].getNotas()[materia] > lista[i].getNotas()[materia]:
                lista[i], lista[j] = lista[j], lista[i]

    print(f"  {'Pos':<5} {'Legajo':<8} {'Nombre':<25} {'Nota':<8} {'Estado'}")
    print(f"  {'-'*5} {'-'*8} {'-'*25} {'-'*8} {'-'*15}")

    pos = 1
    for est in lista:
        nota = est.getNotas()[materia]
        clasif = est.clasificar_nota(nota)
        print(f"  {pos:<5} {est.getLegajo():<8} {est.getNombreCompleto():<25} "
              f"{nota:<8.1f} {clasif}")
        pos += 1

    notas_materia = []
    for est in curso.getEstudiantes():
        notas_materia.append(est.getNotas()[materia])

    print(f"\n  Promedio  : {sum(notas_materia)/len(notas_materia):.2f}")
    print(f"  Nota máx. : {max(notas_materia):.1f}")
    print(f"  Nota mín. : {min(notas_materia):.1f}")

    aprobados = 0
    for n in notas_materia:
        if n >= 6:
            aprobados += 1
    print(f"  Aprobados : {aprobados}/{len(notas_materia)} "
          f"({aprobados/len(notas_materia)*100:.1f}%)")

    pausa()


# ************************************************************
# OPCIÓN 7: GRÁFICO DE BARRAS — PROMEDIO POR ASIGNATURA
# ************************************************************

def opcion_grafico_promedios(curso):
    separador("GENERANDO GRÁFICO: Promedio por Asignatura")

    promedios = curso.promedio_por_asignatura()

    nombres_cortos = {
        "Programación": "Programación",
        "Análisis Estadístico": "Análisis Est.",
        "Base de Datos": "Base de Datos",
        "Arquitecturas en la Nube": "Arq. Nube",
        "Aprendizaje Automático": "Ap. Automático",
        "Captura de la Información": "Cap. Información"
    }

    asignaturas = []
    valores = []
    colores = []
    for materia, prom in promedios.items():
        asignaturas.append(nombres_cortos[materia])
        valores.append(prom)
        if prom >= 6:
            colores.append("slateblue")
        else:
            colores.append("lightskyblue")

    plt.figure(figsize=(10, 6))
    barras = plt.bar(asignaturas, valores, color=colores,
                     edgecolor="white", linewidth=1.5)

    for barra in barras:
        h = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2, h + 0.15,
                 f"{h:.2f}", ha="center", va="bottom",
                 fontweight="bold", fontsize=11)

    plt.axhline(y=6, color="salmon", linestyle="--",
                linewidth=1.5, label="Nota de aprobación (6)")

    plt.title("Promedio por Asignatura",
              fontsize=13, fontweight="bold")
    plt.ylabel("Promedio")
    plt.xlabel("Asignatura")
    plt.ylim(0, 10.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    plt.savefig("grafico_promedio_asignaturas.png", dpi=150)
    plt.show()
    print(f"  Gráfico guardado como 'grafico_promedio_asignaturas.png'")

    pausa()


# ************************************************************
# OPCIÓN 8: GRÁFICO — % APROBACIÓN POR ASIGNATURA
# ************************************************************

def opcion_grafico_aprobacion(curso):
    separador("GENERANDO GRÁFICO: % Aprobación por Asignatura")

    aprobacion = curso.porcentaje_aprobacion_por_asignatura()

    nombres_cortos = {
        "Programación": "Programación",
        "Análisis Estadístico": "Análisis Est.",
        "Base de Datos": "Base de Datos",
        "Arquitecturas en la Nube": "Arq. Nube",
        "Aprendizaje Automático": "Ap. Automático",
        "Captura de la Información": "Cap. Información"
    }

    asignaturas = []
    valores = []
    colores = []
    for materia, pct in aprobacion.items():
        asignaturas.append(nombres_cortos[materia])
        valores.append(pct)
        if pct >= 60:
            colores.append("paleturquoise")
        else:
            colores.append("thistle")

    plt.figure(figsize=(10, 6))
    barras = plt.bar(asignaturas, valores, color=colores,
                     edgecolor="white", linewidth=1.5)

    for barra in barras:
        h = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2, h + 1,
                 f"{h:.1f}%", ha="center", va="bottom",
                 fontweight="bold", fontsize=11)

    plt.axhline(y=60, color="salmon", linestyle="--",
                linewidth=1.5, label="Umbral de aprobación")

    plt.title("Porcentaje de Aprobación por Asignatura",
              fontsize=13, fontweight="bold")
    plt.ylabel("% de Aprobación")
    plt.xlabel("Asignatura")
    plt.ylim(0, 110)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    plt.savefig("grafico_aprobacion_asignaturas.png", dpi=150)
    plt.show()
    print(f"  Gráfico guardado como 'grafico_aprobacion_asignaturas.png'")

    pausa()


# ************************************************************
# OPCIÓN 9: GRÁFICO TORTA — SITUACIÓN ACADÉMICA
# ************************************************************

def opcion_grafico_situacion(curso):
    separador("GENERANDO GRÁFICO: Distribución Académica")

    reprobados = len(curso.estudiantes_reprobados())
    aprobados = curso.getCantidad() - reprobados

    etiquetas = ["Aprobados", "Reprobados"]
    valores = [aprobados, reprobados]
    colores = ["cyan", "dodgerblue"]

    plt.figure(figsize=(8, 6))
    plt.pie(valores, labels=etiquetas, colors=colores,
            autopct="%1.1f%%", startangle=75,
            textprops={"fontsize": 13, "fontweight": "bold"})

    plt.title("Distribución de Situación Académica",
              fontsize=13, fontweight="bold")
    plt.tight_layout()

    plt.savefig("grafico_situacion_academica.png", dpi=150)
    plt.show()
    print(f"  Gráfico guardado como 'grafico_situacion_academica.png'")

    pausa()


# ************************************************************
# MENÚ PRINCIPAL
# ************************************************************

def mostrar_menu():
    print("\n" + "*" * 60)
    print("   SISTEMA DE EVALUACIÓN ESTUDIANTIL")
    print("*" * 60)
    print("")
    print("   REPORTES POR CONSOLA")
    print("    1. Ver listado completo de estudiantes")
    print("    2. Buscar estudiante por legajo")
    print("    3. Ver promedio individual por estudiante")
    print("    4. Ver estadísticas generales del curso")
    print("    5. Ver promedio por asignatura")
    print("    6. Ver detalle por materia")
    print("")
    print("   GRÁFICOS")
    print("    7. Gráfico: Promedio por asignatura")
    print("    8. Gráfico: % Aprobación por asignatura")
    print("    9. Gráfico: Distribución académica (torta)")
    print("")
    print("    0. Salir")
    print("*" * 60)


def ejecutar_menu():
    """Bucle principal del menú interactivo."""

    curso = Curso(ARCHIVO)

    if curso.getCantidad() == 0:
        print("\n  Error: No se pudieron cargar estudiantes.")
        print("  Ejecute primero el Módulo 1 (estudiantes_csv.py).")
        return

    while True:
        mostrar_menu()
        eleccion = input("\n  Seleccione una opción: ").strip()

        if eleccion == "0":
            print("\n  Gracias por utilizar el sistema, hasta luego.\n")
            break
        elif eleccion == "1":
            opcion_listado(curso)
        elif eleccion == "2":
            opcion_buscar_legajo(curso)
        elif eleccion == "3":
            opcion_promedio_individual(curso)
        elif eleccion == "4":
            opcion_promedio_general(curso)
        elif eleccion == "5":
            opcion_promedio_asignatura(curso)
        elif eleccion == "6":
            opcion_detalle_materia(curso)
        elif eleccion == "7":
            opcion_grafico_promedios(curso)
        elif eleccion == "8":
            opcion_grafico_aprobacion(curso)
        elif eleccion == "9":
            opcion_grafico_situacion(curso)
        else:
            print("  Error: Opción no válida. Intente nuevamente.")


# ************************************************************
# PUNTO DE ENTRADA
# ************************************************************

if __name__ == "__main__":
    ejecutar_menu()
