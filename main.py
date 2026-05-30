import sys
from lexer import lexer, errores_lexicos
from parser import parser, reiniciar_errores_sintaxis
from parser import errores as errores_sintaxis
from errores_reporte import establecer_codigo, formatear_error
from validacion_semantica import validar as validar_semantica


def normalizar_codigo(codigo):
    """Convierte comillas tipográficas del PDF a comillas ASCII."""
    return (
        codigo.replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u00ab", '"')
        .replace("\u00bb", '"')
    )


def compilar_codigo(codigo):
    codigo = normalizar_codigo(codigo)
    establecer_codigo(codigo)
    lexer.lineno = 1
    reiniciar_errores_sintaxis()
    errores_lexicos.clear()

    parser.parse(codigo, lexer=lexer)

    detalles = errores_lexicos + errores_sintaxis
    if len(detalles) == 0:
        detalles = validar_semantica(codigo)
    if len(detalles) == 0:
        return {"exito": True, "errores": [], "detalles": []}

    return {
        "exito": False,
        "errores": [formatear_error(d) for d in detalles],
        "detalles": detalles,
    }


def compilar(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        detalle = {
            "tipo": "archivo",
            "linea": 0,
            "columna": 0,
            "mensaje": f"No se encontró el archivo: {nombre_archivo}",
            "sugerencia": "Verifica la ruta y el nombre del archivo.",
            "linea_codigo": "",
            "puntero": "",
        }
        return {
            "exito": False,
            "errores": [formatear_error(detalle)],
            "detalles": [detalle],
        }

    resultado = compilar_codigo(codigo)
    if resultado["exito"]:
        print("Compilado correctamente")
    else:
        for error in resultado["errores"]:
            print(error)
            print()
    return resultado


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.txt")
    else:
        compilar(sys.argv[1])
