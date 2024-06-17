import ply.lex as lex

# Lista de tokens
tokens = (
    'NUMBER',
    'FOR',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'EQUALS',
    'RELOP',
    'PLUSPLUS',
    'PRINT1',
    'PRINT2',
    'PRINT3',
    'FALSE',
    'PUNTO',
    'STRING',
    'IF',
    'ELSE',
    'WHILE',
    'INT',
    'FLOAT',
    'STRING_TYPE'
    # ... aquí puedes agregar más tokens según tus necesidades

)

# Expresiones regulares para tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_RELOP = r'(<=|>=|==|!=|<|>)'
t_PLUSPLUS = r'\+\+'
t_PUNTO = r'.'

# Expresiones regulares para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    palabras_reservadas = {
    'int': 'INT',
    'float': 'FLOAT',
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'system' : 'PRINT1',
    'out' : 'PRINT2',
    'println' : 'PRINT3',
        # ... más palabras reservadas pueden ser añadidas aquí
    }
    t.type = palabras_reservadas.get(t.value, 'ID')  # Si no es palabra reservada, es un ID
    return t

def t_STRING_TYPE(t):
    r'string'
    return t

# Expresiones regulares para números
# def t_FLOAT(t):
#     r'\d+\.\d+'
#     t.value = float(t.value)
#     return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Expresiones regulares para cadenas de texto
def t_STRING(t):
    r'(\'[^\']*\'|\"[^\"]*\")'  # Esta expresión regular coincide con comillas simples o dobles
    t.value = t.value[1:-1]  # Elimina las comillas alrededor de la cadena
    return t

# Expresiones regulares para caracteres individuales
def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1]
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_space(t):
    r'\s+'
    t.lexer.lineno += len(t.value)
        
# Ignorar caracteres como espacios y saltos de línea
t_ignore = '\t'

# def t_MAS_MAS(t):
#     r'\+\+'
#     return t

# def t_MENORIGUAL(t):
#     r'<='
#     return t

# def t_MAYORIGUAL(t):
#     r'>='
#     return t

# def t_IGUAL(t):
#     r'=='
#     return t

# def t_DIFERENTE(t):
#     r'!='
#     return t


# # Expresión regular para comentarios de una sola línea
# def t_COMENTARIO_UNA_LINEA(t):
#     r'\#.*'
#     t.value = t.value[1:]  # Elimina el signo de número (#) del comentario
#     return t

# Manejo de errores léxicos
def t_error(t):
    print("Ilegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t


# instanciamos el analizador lexico
lexer = lex.lex()

def tokenize(data):
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
    return tokens