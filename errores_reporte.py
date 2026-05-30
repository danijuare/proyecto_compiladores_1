"""Utilidades para reportar errores con línea, columna y contexto."""

_codigo_fuente = ""

TOKEN_A_TEXTO = {
    "PROGRAMA": "Programa",
    "ENTERO": "entero",
    "DECIMAL": "decimal",
    "DOBLE": "doble",
    "CARACTER": "caracter",
    "BOLEANO": "boleano",
    "CONSTANTE": "constante",
    "SI": "si",
    "MIENTRAS": "mientras",
    "PARA": "para",
    "HACER": "hacer",
    "CASOS": "casos",
    "CASO": "Caso",
    "DEFECTO": "defecto",
    "PARAR": "parar",
    "RETORNAR": "retornar",
    "DELOCONTRARIO": "delocontrario",
    "INGRESAR": "Ingresar",
    "IMPRIMIR": "Imprimir",
    "VERDADERO": "verdadero",
    "PUNTOCOMA": "';'",
    "COMA": "','",
    "PARIZQ": "'('",
    "PARDER": "')'",
    "LLAVEIZQ": "'{'",
    "LLAVEDER": "'}'",
    "CORCHETEIZQ": "'['",
    "CORCHETEDER": "']'",
    "IGUAL": "'='",
    "DOSPUNTOS": "':'",
    "PUNTO": "'.'",
    "ID": "identificador",
    "NUMERO": "número",
    "CADENA": "cadena de texto",
}


def establecer_codigo(codigo):
    global _codigo_fuente
    _codigo_fuente = codigo


def columna_desde_lexpos(lexpos):
    if lexpos is None or lexpos < 0:
        return 1
    return len(_codigo_fuente[:lexpos].split("\n")[-1]) + 1


def fragmento_linea(lineno, columna):
    lineas = _codigo_fuente.split("\n")
    if lineno < 1 or lineno > len(lineas):
        return "", ""
    linea = lineas[lineno - 1].expandtabs(4).rstrip()
    col = max(1, min(columna, len(linea) + 1))
    puntero = " " * (col - 1) + "^"
    return linea, puntero


def _token_legible(tipo, valor):
    if tipo in TOKEN_A_TEXTO:
        return TOKEN_A_TEXTO[tipo]
    if valor is not None:
        return repr(valor)
    return tipo or "fin de archivo"


def _sugerencia_lexico(caracter):
    if caracter in '"“”«»':
        return "Usa comillas rectas ASCII: \"texto\""
    if caracter in "'‘’":
        return "Las cadenas deben ir entre comillas dobles: \"texto\""
    if caracter == "@":
        return "El símbolo '@' no pertenece al lenguaje."
    return "Elimina o corrige ese carácter; revisa la sintaxis del enunciado."


def _sugerencia_sintaxis(tipo, valor, lineno):
    if tipo in (
        "ENTERO",
        "DECIMAL",
        "DOBLE",
        "CARACTER",
        "BOLEANO",
        "CONSTANTE",
        "SI",
        "MIENTRAS",
        "PARA",
        "CASOS",
        "RETORNAR",
        "IMPRIMIR",
        "INGRESAR",
        "ID",
    ):
        if lineno > 1:
            return (
                "Suele faltar un punto y coma (;) al final de la sentencia "
                f"en la línea {lineno - 1}."
            )
        return "Revisa la estructura del programa; debe iniciar con Programa nombre() { }."

    if tipo == "PUNTOCOMA":
        return "El ';' aparece en un lugar donde no se esperaba."

    if tipo == "PARIZQ":
        return "Hay un '(' de más o falta cerrar una expresión antes."

    if tipo == "PARDER":
        return "Falta un paréntesis de apertura '(' o hay un ')' de más."

    if tipo == "LLAVEIZQ":
        return "Hay una llave '{' en un lugar no válido."

    if tipo == "LLAVEDER":
        return "Falta una llave de apertura '{' o hay un '}' de más."

    if tipo == "CORCHETEDER":
        return "Falta '[' al declarar el arreglo o hay un ']' de más."

    if tipo == "CORCHETEIZQ":
        return "El '[' aparece donde no se espera un arreglo."

    if tipo == "PARAR":
        return "En un Caso, las sentencias deben terminar con parar; antes del siguiente Caso."

    if tipo == "CASO":
        return "Dentro de casos { } cada opción debe ser: Caso número: sentencias parar;"

    if tipo == "COMA":
        return "Revisa las comas en parámetros o en la lista de variables."

    if valor == ";":
        return "Revisa que cada sentencia termine con ; en el lugar correcto."

    return "Revisa la sintaxis cerca de esa posición según los ejemplos del enunciado."


def error_lexico(lineno, lexpos, caracter):
    col = columna_desde_lexpos(lexpos)
    linea, puntero = fragmento_linea(lineno, col)
    sugerencia = _sugerencia_lexico(caracter)
    return {
        "tipo": "léxico",
        "linea": lineno,
        "columna": col,
        "mensaje": f"Carácter no válido: '{caracter}'",
        "sugerencia": sugerencia,
        "linea_codigo": linea,
        "puntero": puntero,
    }


def error_sintaxis(token):
    if token is None:
        lineas = _codigo_fuente.split("\n")
        lineno = len(lineas) if lineas else 1
        col = 1
        if lineas:
            col = len(lineas[-1].expandtabs(4)) + 1
        linea, puntero = fragmento_linea(lineno, col)
        return {
            "tipo": "sintaxis",
            "linea": lineno,
            "columna": col,
            "mensaje": "Fin inesperado del archivo",
            "sugerencia": (
                "Faltan llaves '}', paréntesis ')' o punto y coma ';' "
                "para cerrar el programa."
            ),
            "linea_codigo": linea,
            "puntero": puntero,
        }

    col = columna_desde_lexpos(token.lexpos)
    legible = _token_legible(token.type, token.value)
    linea, puntero = fragmento_linea(token.lineno, col)
    sugerencia = _sugerencia_sintaxis(token.type, token.value, token.lineno)

    return {
        "tipo": "sintaxis",
        "linea": token.lineno,
        "columna": col,
        "mensaje": f"Elemento inesperado ({legible}): '{token.value}'",
        "sugerencia": sugerencia,
        "linea_codigo": linea,
        "puntero": puntero,
    }


def formatear_error(detalle):
    """Texto multilínea para consola."""
    lineas = [
        f"Error {detalle['tipo']} en linea {detalle['linea']}, columna {detalle['columna']}",
        f"  > {detalle['mensaje']}",
        f"  > {detalle['sugerencia']}",
    ]
    if detalle.get("linea_codigo"):
        num = detalle["linea"]
        lineas.append("")
        lineas.append(f"  {num:>4} | {detalle['linea_codigo']}")
        lineas.append(f"       | {detalle['puntero']}")
    return "\n".join(lineas)
