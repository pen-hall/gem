#############################
#      CONSTANTS
#############################

DIGITS = '0123456789'

#tokens
TT_INT     = 'TT_INT'
TT_FLOAT   = 'FLOAT'
TT_PLUS    = 'PLUS'
TT_MINUS   = 'MINUS'
TT_MUL     = 'MUL'
TT_DIV     = 'DIV'
TT_LPAREN  = 'LPAREN'
TT_RPAREN  = 'RPAREN'

#############################
#      ERRORS
#############################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File: {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'IllegalCharError', details)

#############################
#      POSISTION
#############################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#############################
#      TOKENS
#############################


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    

#############################
#      LEXER
#############################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        #print("advance")
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None


    def make_tokens(self):
        tokens = []
        #print("tokens")

        while self.current_char != None:
            if self.current_char in ' \t':
                #print("space or tab")
                self.advance()

            elif self.current_char in DIGITS:
                #print("digit")
                tokens.append(self.make_number())
                self.advance()

            elif self.current_char == '+':
                #print("+")
                tokens.append(Token(TT_PLUS))  
                self.advance()
            elif self.current_char == '-':
                #print("-")
                tokens.append(Token(TT_MINUS))   
                self.advance()
            elif self.current_char == '*':
                #print("*")
                tokens.append(Token(TT_MUL))  
                self.advance()
            elif self.current_char == '/':
                #print("/")
                tokens.append(Token(TT_DIV))   
                self.advance()
            elif self.current_char == '(':
                #print("(")
                tokens.append(Token(TT_LPAREN)) 
                self.advance()
            elif self.current_char == ')':
                #print(")")
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:#error
                self.pos_start = self.pos.copy()
                char = self.current_char
                #print("illegal char")
                self.advance
                return [], IllegalCharError(self.pos_start, self.pos, "'" + char + "'")
            #print("End loop in make token")

        #print("make tokens")
        return tokens, None
    
    def make_number(self):
        #print("number")
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break #make this return some error maybe?
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


#############################
#      RUN
#############################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error