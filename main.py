import sys
from lexer import lexer, errores_lexicos
from parser import parser, errores


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
    lexer.lineno = 1
    errores.clear()
    errores_lexicos.clear()

    parser.parse(codigo, lexer=lexer)

    todos_errores = errores_lexicos + errores
    if len(todos_errores) == 0:
        return {"exito": True, "errores": []}
    return {"exito": False, "errores": todos_errores}


def compilar(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        return {
            "exito": False,
            "errores": [f"No se encontró el archivo: {nombre_archivo}"],
        }

    resultado = compilar_codigo(codigo)
    if resultado["exito"]:
        print("Compilado correctamente")
    else:
        for error in resultado["errores"]:
            print(error)
    return resultado


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.txt")
    else:
        compilar(sys.argv[1])
