import ply.yacc as yacc
from lexer import tokens

errores = []

def p_programa(p):
    '''
    programa : PROGRAMA ID PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER
    '''
    p[0] = "Programa válido"

def p_sentencias(p):
    '''
    sentencias : sentencias sentencia
               | sentencia
               | empty
    '''

def p_sentencia(p):
    '''
    sentencia : declaracion_o_funcion
              | declaracion_arreglo
              | asignacion
              | imprimir
              | ingresar
              | si
              | mientras
              | para
              | casos
              | retornar
              | procedimiento
    '''

def p_tipo(p):
    '''
    tipo : ENTERO
         | DECIMAL
         | DOBLE
         | CARACTER
         | BOLEANO
    '''

def p_declaracion_o_funcion(p):
    '''
    declaracion_o_funcion : tipo ID PUNTOCOMA
                          | tipo ID PARIZQ parametros_funcion PARDER LLAVEIZQ sentencias LLAVEDER
                          | CONSTANTE tipo ID IGUAL expresion PUNTOCOMA
    '''

def p_declaracion_arreglo(p):
    '''
    declaracion_arreglo : tipo ID CORCHETEIZQ dimensiones CORCHETEDER PUNTOCOMA
    '''

def p_dimensiones(p):
    '''
    dimensiones : NUMERO
                | dimensiones COMA NUMERO
    '''

def p_asignacion(p):
    '''
    asignacion : ID IGUAL expresion PUNTOCOMA
               | ID IGUAL INGRESAR PARIZQ parametro_unico PARDER PUNTOCOMA
    '''

def p_ingresar(p):
    '''
    ingresar : INGRESAR PARIZQ parametro_unico PARDER PUNTOCOMA
    '''

def p_parametro_unico(p):
    '''
    parametro_unico : expresion
    '''

def p_imprimir(p):
    '''
    imprimir : IMPRIMIR PARIZQ parametros PARDER PUNTOCOMA
    '''

def p_parametros(p):
    '''
    parametros : expresion
               | parametros COMA expresion
               | parametros PUNTO expresion
               | empty
    '''

def p_si(p):
    '''
    si : SI PARIZQ condicion PARDER LLAVEIZQ sentencias LLAVEDER
       | SI PARIZQ condicion PARDER LLAVEIZQ sentencias LLAVEDER DELOCONTRARIO LLAVEIZQ sentencias LLAVEDER
    '''

def p_mientras(p):
    '''
    mientras : MIENTRAS PARIZQ condicion PARDER LLAVEIZQ sentencias LLAVEDER
    '''

def p_para(p):
    '''
    para : PARA PARIZQ inicializacion_para PUNTOCOMA condicion PUNTOCOMA paso_para PARDER HACER LLAVEIZQ sentencias LLAVEDER
         | PARA PARIZQ inicializacion_para PUNTOCOMA condicion PUNTOCOMA paso_para PARDER LLAVEIZQ sentencias LLAVEDER
    '''

def p_inicializacion_para(p):
    '''
    inicializacion_para : ID
                        | ID IGUAL expresion
                        | tipo ID
                        | tipo ID IGUAL expresion
    '''

def p_paso_para(p):
    '''
    paso_para : ID IGUAL expresion
    '''

def p_casos(p):
    '''
    casos : CASOS ID LLAVEIZQ lista_casos defecto LLAVEDER
    '''

def p_lista_casos(p):
    '''
    lista_casos : lista_casos caso
                | caso
    '''

def p_caso(p):
    '''
    caso : CASO NUMERO DOSPUNTOS sentencias PARAR PUNTOCOMA
    '''

def p_defecto(p):
    '''
    defecto : DEFECTO DOSPUNTOS sentencias
            | empty
    '''

def p_procedimiento(p):
    '''
    procedimiento : ID PARIZQ parametros_funcion PARDER LLAVEIZQ sentencias LLAVEDER
    '''

def p_parametros_funcion(p):
    '''
    parametros_funcion : tipo ID opcion_mas_params
                       | empty
    '''

def p_opcion_mas_params(p):
    '''
    opcion_mas_params : COMA tipo ID opcion_mas_params
                      | COMA mas_ids
                      | empty
    '''

def p_mas_ids(p):
    '''
    mas_ids : ID
            | mas_ids COMA ID
    '''

def p_retornar(p):
    '''
    retornar : RETORNAR PARIZQ expresion PARDER PUNTOCOMA
    '''

def p_condicion(p):
    '''
    condicion : expresion operador_relacional expresion
              | VERDADERO
    '''

def p_operador_relacional(p):
    '''
    operador_relacional : MAYOR
                        | MENOR
                        | MAYORIGUAL
                        | MENORIGUAL
                        | IGUALIGUAL
                        | DIFERENTE
    '''

def p_expresion(p):
    '''
    expresion : expresion MAS termino
              | expresion MENOS termino
              | termino
    '''

def p_termino(p):
    '''
    termino : termino POR factor
            | termino DIVIDIDO factor
            | factor
    '''

def p_factor(p):
    '''
    factor : NUMERO
           | CADENA
           | ID
           | VERDADERO
           | PARIZQ expresion PARDER
    '''

def p_empty(p):
    '''
    empty :
    '''

def p_error(p):
    if p:
        mensaje = f"Error de sintaxis en línea {p.lineno}: cerca de '{p.value}'"
    else:
        mensaje = "Error de sintaxis: final inesperado del archivo"

    errores.append(mensaje)

parser = yacc.yacc()