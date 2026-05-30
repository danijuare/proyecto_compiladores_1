import ply.lex as lex

reserved = {
    'Programa': 'PROGRAMA',
    'boleano': 'BOLEANO',
    'decimal': 'DECIMAL',
    'verdadero': 'VERDADERO',
    'caracter': 'CARACTER',
    'entero': 'ENTERO',
    'doble': 'DOBLE',
    'constante': 'CONSTANTE',
    'casos': 'CASOS',
    'defecto': 'DEFECTO',
    'Caso': 'CASO',
    'parar': 'PARAR',
    'para': 'PARA',
    'hacer': 'HACER',
    'mientras': 'MIENTRAS',
    'retornar': 'RETORNAR',
    'si': 'SI',
    'delocontrario': 'DELOCONTRARIO',
    'procedimiento': 'PROCEDIMIENTO',
    'Ingresar': 'INGRESAR',
    'Imprimir': 'IMPRIMIR'
}

tokens = [
    'ID',
    'NUMERO',
    'CADENA',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'IGUAL',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'PUNTO',
    'COMA',
    'PUNTOCOMA',
    'DOSPUNTOS',
    'PARIZQ',
    'PARDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'CORCHETEIZQ',
    'CORCHETEDER'
] + list(reserved.values())

t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUALIGUAL = r'=='
t_DIFERENTE = r'!='
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_PUNTO = r'\.'
t_COMA = r','
t_PUNTOCOMA = r';'
t_DOSPUNTOS = r':'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_CORCHETEIZQ = r'\['
t_CORCHETEDER = r'\]'

t_ignore = ' \t'

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    return t

def t_ID(t):
    r'[a-zA-Z_áéíóúÁÉÍÓÚñÑ][a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMENTARIO(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

errores_lexicos = []

def t_error(t):
    from errores_reporte import error_lexico

    errores_lexicos.append(error_lexico(t.lineno, t.lexpos, t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()