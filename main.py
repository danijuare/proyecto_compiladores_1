import sys
from lexer import lexer
from parser import parser, errores

def compilar(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()

        lexer.lineno = 1
        errores.clear()

        resultado = parser.parse(codigo, lexer=lexer)

        if len(errores) == 0:
            print("Compilado correctamente")
        else:
            for error in errores:
                print(error)

    except FileNotFoundError:
        print("No se encontró el archivo:", nombre_archivo)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.txt")
    else:
        compilar(sys.argv[1])