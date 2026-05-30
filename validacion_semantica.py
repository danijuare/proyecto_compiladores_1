"""Validaciones después del análisis sintáctico."""

from errores_reporte import (
    columna_desde_lexpos,
    establecer_codigo,
    fragmento_linea,
)

from lexer import lexer

TIPOS = {"ENTERO", "DECIMAL", "DOBLE", "CARACTER", "BOLEANO"}


def _tokenizar(codigo):
    lexer.lineno = 1
    lexer.input(codigo)
    return list(lexer)


def _extraer_parentesis(tokens, inicio):
    """inicio apunta al token PARIZQ. Devuelve (tokens_internos, indice_cierre)."""
    if inicio >= len(tokens) or tokens[inicio].type != "PARIZQ":
        return [], inicio
    profundidad = 0
    internos = []
    i = inicio
    while i < len(tokens):
        if tokens[i].type == "PARIZQ":
            profundidad += 1
            if profundidad > 1:
                internos.append(tokens[i])
        elif tokens[i].type == "PARDER":
            profundidad -= 1
            if profundidad == 0:
                return internos, i
            internos.append(tokens[i])
        else:
            if profundidad > 0:
                internos.append(tokens[i])
        i += 1
    return internos, inicio


def _extraer_parametros_funcion(tokens, inicio):
    """Tras tipo ID PARIZQ, extrae nombres de parámetros."""
    internos, _ = _extraer_parentesis(tokens, inicio)
    nombres = []
    i = 0
    while i < len(internos):
        if internos[i].type in TIPOS and i + 1 < len(internos) and internos[i + 1].type == "ID":
            nombres.append(internos[i + 1].value)
            i += 2
            if i < len(internos) and internos[i].type == "COMA":
                i += 1
            continue
        i += 1
    return nombres


def _recolectar_declarados(tokens):
    declarados = set()
    i = 0
    n = len(tokens)

    while i < n:
        t = tokens[i]

        if t.type == "CONSTANTE" and i + 2 < n:
            if tokens[i + 1].type in TIPOS and tokens[i + 2].type == "ID":
                declarados.add(tokens[i + 2].value)
                i += 3
                continue

        if t.type in TIPOS and i + 1 < n and tokens[i + 1].type == "ID":
            declarados.add(tokens[i + 1].value)
            if i + 2 < n and tokens[i + 2].type == "PARIZQ":
                declarados.update(_extraer_parametros_funcion(tokens, i + 2))
            i += 2
            continue

        if (
            t.type == "ID"
            and i + 1 < n
            and tokens[i + 1].type == "PARIZQ"
            and (i == 0 or tokens[i - 1].type not in TIPOS)
        ):
            declarados.update(_extraer_parametros_funcion(tokens, i + 1))
            i += 2
            continue

        if t.type == "PARA" and i + 1 < n and tokens[i + 1].type == "PARIZQ":
            internos, cierre = _extraer_parentesis(tokens, i + 1)
            j = 0
            while j < len(internos):
                if internos[j].type in TIPOS and j + 1 < len(internos):
                    if internos[j + 1].type == "ID":
                        declarados.add(internos[j + 1].value)
                        j += 2
                        continue
                if internos[j].type == "ID" and j + 1 < len(internos) and internos[j + 1].type == "IGUAL":
                    declarados.add(internos[j].value)
                j += 1
            i = cierre + 1
            continue

        i += 1

    return declarados


def _error_semantico(lineno, lexpos, mensaje, sugerencia):
    col = columna_desde_lexpos(lexpos)
    linea, puntero = fragmento_linea(lineno, col)
    return {
        "tipo": "semántico",
        "linea": lineno,
        "columna": col,
        "mensaje": mensaje,
        "sugerencia": sugerencia,
        "linea_codigo": linea,
        "puntero": puntero,
    }


def _atomos_en_parametros(args_tokens):
    return [
        t
        for t in args_tokens
        if t.type in ("CADENA", "ID", "NUMERO", "VERDADERO")
    ]


def validar(codigo):
    establecer_codigo(codigo)
    tokens = _tokenizar(codigo)
    declarados = _recolectar_declarados(tokens)
    errores = []
    i = 0
    n = len(tokens)

    while i < n:
        if tokens[i].type not in ("IMPRIMIR", "INGRESAR"):
            i += 1
            continue

        es_ingresar = tokens[i].type == "INGRESAR"
        if i + 1 >= n or tokens[i + 1].type != "PARIZQ":
            i += 1
            continue

        args_tokens, cierre = _extraer_parentesis(tokens, i + 1)
        atomos = _atomos_en_parametros(args_tokens)

        if es_ingresar:
            if len(atomos) == 0:
                pass
            elif atomos[0].type != "CADENA":
                nombre = atomos[0].value
                errores.append(
                    _error_semantico(
                        atomos[0].lineno,
                        atomos[0].lexpos,
                        f"Ingresar(...) requiere un texto entre comillas, no '{nombre}'.",
                        f'Usa: Ingresar("{nombre}")',
                    )
                )
        else:
            for atom in atomos:
                if atom.type == "ID" and atom.value not in declarados:
                    nombre = atom.value
                    errores.append(
                        _error_semantico(
                            atom.lineno,
                            atom.lexpos,
                            f"'{nombre}' no es una variable declarada ni una cadena.",
                            f'Si es texto, escribe comillas: Imprimir("{nombre}")',
                        )
                    )

        i = cierre + 1

    return errores
