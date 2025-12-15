# =====================
# TOKEN & TOKEN TYPE
# =====================
class TokenType:
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


# =====================
# LEXER
# =====================
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        num = ""
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return int(num)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            raise Exception(f"Karakter tidak dikenal: {self.current_char}")

        return Token(TokenType.EOF)


# =====================
# PARSER
# =====================
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    # factor : INTEGER | LPAREN expr RPAREN
    def factor(self):
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.expr()
            self.eat(TokenType.RPAREN)

        else:
            self.error()

    # term : factor ((MULTIPLY | DIVIDE) factor)*
    def term(self):
        self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            self.eat(self.current_token.type)
            self.factor()

    # expr : term ((PLUS | MINUS) term)*
    def expr(self):
        self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            self.eat(self.current_token.type)
            self.term()

    def parse(self):
        self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error()
        return True


# =====================
# VALIDATION HELPER
# =====================
def validate_expression(text):
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        parser.parse()
        return "valid"
    except Exception:
        return "invalid"


# =====================
# TEST
# =====================
print(validate_expression("10 + 2 * (5 - 3)"))  # valid
print(validate_expression("10 + * "))           # invalid
print(validate_expression("(1 + 2) * 3"))       # valid
print(validate_expression("5 + (3 * )"))        # invalid
