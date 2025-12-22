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
        return f"{self.type}:{self.value}"


# =====================
# AST NODES
# =====================
class AST:
    pass


class NumberNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Number({self.value})"


class BinOpNode(AST):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

    def __repr__(self):
        return f"({self.op_token.value} {self.left} {self.right})"


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
# PARSER (RETURN AST)
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
            return NumberNode(token)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        else:
            self.error()

    # term : factor ((MULTIPLY | DIVIDE) factor)*
    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token
            self.eat(op.type)
            node = BinOpNode(node, op, self.factor())

        return node

    # expr : term ((PLUS | MINUS) term)*
    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.eat(op.type)
            node = BinOpNode(node, op, self.term())

        return node

    def parse(self):
        node = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error()
        return node


# =====================
# TEST AST
# =====================
text = "3 * (4 + 5)"
lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()

print(ast)
