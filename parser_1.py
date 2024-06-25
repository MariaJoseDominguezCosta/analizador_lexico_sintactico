import ply.yacc as yacc
from lexer import tokens

# Tabla de símbolos
symbol_table = {}

errores = []
# Definición de precedencia y asociatividad de los operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),  # Unary minus operator
)
def p_program(t):
    '''program : statement_list'''
    t[0] = t[1]

def p_statement_list(p):
    '''statement_list : statement
    | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
        
def p_statement(t):
    '''statement : declaration
                | for_statement
                | assignment
                | print
                | block'''
    t[0] = [t[1]]   
def p_statement_for(t):
    '''for_statement : FOR LPAREN for_declaration expression SEMICOLON expression RPAREN LBRACE statement RBRACE'''
    t[0] = ('for', t[4], t[9])

def p_for_declaration(t):
    '''for_declaration : declaration
                    | ID EQUALS expression SEMICOLON'''
    t[0] = t[1]


def p_declaration(t):
    '''declaration : type ID EQUALS expression SEMICOLON
    | type ID SEMICOLON'''
    if len(t) == 4:
        if t[2] in symbol_table:
            errores.append(f"Error: Variable '{t[2]}' ya declarada.")
        else:
            symbol_table[t[2]] = t[1]
            t[0] = ('declaration', t[1], t[2])
    else:
        if t[2] in symbol_table:
            errores.append(f"Error: Variable '{t[2]}' ya declarada.")
        else:
            symbol_table[t[2]] = t[1]
            t[0] = ('declaration', t[1], t[2], t[4])

def p_type(t):
    '''type : INT
            | FLOAT
            | STRING_TYPE'''
    t[0] = t[1]

def p_expression(t):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | MINUS expression %prec UMINUS
                | NUMBER
                | ID
                | ID PLUSPLUS
                | ID RELOP expression'''
    if len(t) == 4:
        if t[2] == '+':
            t[0] = t[1] + t[3]
        elif t[2] == '-':
            t[0] = t[1] - t[3]
        elif t[2] == '*':
            t[0] = t[1] * t[3]
        elif t[2] == '/':
            t[0] = t[1] / t[3]
        elif t[2] == '++':
            t[0] = t[1] + 1
        elif t[2] in ('<=', '>=', '==', '!=', '<', '>'):
            t[0] = (t[2], t[1], t[3])
    elif len(t) == 3:
        if t[1] == '-':
            t[0] = -t[2]
    else:
        t[0] = t[1]

    # Verificar uso de variables no declaradas
    if isinstance(t[1], str) and t[1] not in symbol_table:
        errores.append(f"Error: Variable '{t[1]}' no declarada.")

def p_statement_print(t):
    '''print : PRINT1 PUNTO PRINT2 PUNTO PRINT3 LPAREN STRING PLUS expression RPAREN SEMICOLON
    | PRINT1 PUNTO PRINT2 PUNTO PRINT3 LPAREN expression RPAREN SEMICOLON'''
    t[0] = f"Print: {t[3]} {t[5]}"

def p_statement_if(t):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE
                | IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    if len(t) == 8:
        t[0] = ("if", t[3], t[6])
    else:
        t[0] = ("if-else", t[3], t[6], t[10])

def p_statement_while(t):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statement RBRACE'''
    t[0] = ("while", t[3], t[6])

def p_statement_assign(t):
    '''assignment : ID EQUALS expression SEMICOLON'''
    var_name = t[1]
    if var_name not in symbol_table:
        errores.append(f"Error: Variable '{var_name}' no declarada.")
    else:
        t[0] = ("assign", var_name, t[3])

def p_block(t):
    '''block : LBRACE statement RBRACE'''
    t[0] = t[2]
    


# Regla para errores de sintaxis
def p_error(p):
    if p:
        error_message = (
            f"Error de sintaxis en la posición {p.lexpos}: Token '{p.value}' inesperado"
        )
    else:
        error_message = "Error de sintaxis: se expera un token"
    raise SyntaxError(error_message)


# Instanciar el analizador
parser = yacc.yacc()


# Función para analizar una expresión
def parse(expression):
    global symbol_table
    global errores

    # Reiniciar tabla de símbolos y errores
    error_message = None  # Inicializa la variable error_message
    resultado = None  # Inicializa la variable resultado
    try:
        resultado = parser.parse(expression)
        if resultado is not None:
            return str(resultado) + " ,Sintaxis correcta"
        else:
            return "Sintaxis correcta"

    except SyntaxError as e:
        error_message = str(e)
        print("Error:", error_message)
        return error_message
