# Proyecto final de Compiladores

Compilador del lenguaje en español definido en el curso. Implementa **analizador léxico** y **analizador sintáctico** con [PLY](https://www.dabeaz.com/ply/) (equivalente a Lex/Yacc).

## Requisitos

- Python 3.10 o superior
- PLY: `pip install -r requirements.txt`

## Ejecución

### Consola (archivo de entrada)

```bash
python main.py prueba_1.txt
```

Muestra `Compilado correctamente` o los errores con número de línea.

### Interfaz web (HTML/CSS)

```bash
pip install flask
python web_app.py
```

Abre en el navegador: **http://127.0.0.1:5000**

Interfaz para abrir `.txt`, cargar ejemplos, editar código y compilar con **F5**.

## Archivos del proyecto

| Archivo | Descripción |
|---------|-------------|
| `lexer.py` | Analizador léxico (tokens y palabras reservadas) |
| `parser.py` | Gramática y analizador sintáctico |
| `main.py` | Punto de entrada por consola |
| `web_app.py` | Servidor de la interfaz web |
| `web/` | Interfaz HTML, CSS y JavaScript |
| `prueba_*.txt` | Programas de prueba del enunciado |

## Pruebas incluidas

- `prueba_1.txt` — Ejemplo 1 (si / delocontrario, Ingresar, Imprimir)
- `prueba_2.txt` — Ejemplo 2 (mientras)
- `prueba_3.txt` — Ejemplo 3 (casos / Caso / defecto / parar)
- `prueba_correcta.txt` — Programa válido adicional
- `prueba_error.txt` — Programa con error de sintaxis (prueba de detección)
- `prueba_para.txt` — Bucle `para` / `hacer`
- `prueba_funcion.txt` — Declaración de función y `retornar`
- `prueba_procedimiento.txt` — Procedimiento con parámetros `entero a, b`

## Sintaxis soportada (resumen)

- `Programa nombre() { sentencias }`
- Tipos: `entero`, `decimal`, `doble`, `caracter`, `boleano`, `constante`
- Arreglos: `tipo nombre[tam]` o `tipo nombre[t1,t2,...]`
- `si`, `delocontrario`, `mientras`, `para (...) hacer { }`
- `casos variable { Caso n: ... parar; defecto: ... }`
- `Ingresar(expresion)` — un parámetro
- `Imprimir(a, b, ...)` o concatenación con `.`
- Funciones y procedimientos con parámetros tipados
