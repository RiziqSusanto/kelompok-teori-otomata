import string

# =========================
# TOKEN DEFINITIONS
# =========================

TT_INTEGER   = 'INTEGER'
TT_PLUS      = 'PLUS'
TT_MINUS     = 'MINUS'
TT_MULTIPLY  = 'MULTIPLY'
TT_DIVIDE    = 'DIVIDE'
TT_LPAREN    = 'LPAREN'
TT_RPAREN    = 'RPAREN'
TT_EOF       = 'EOF'

TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD    = 'KEYWORD'
TT_EQ         = 'EQ'

KEYWORDS = ["var", "if", "else"]

LETTERS = string.ascii_letters
LETTER_DIGITS = LETTERS + string.digits + "_"


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


# =========================
# LEXER
# =========================

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_integer(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TT_INTEGER, int(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and self.current_char in LETTER_DIGITS:
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str)

    def generate_tokens(self):
        tokens = []

        while self.current_char is not None:

            if self.current_char.isspace():
                self.advance()

            elif self.current_char.isdigit():
                tokens.append(self.make_integer())

            elif self.current_char in LETTERS or self.current_char == "_":
                tokens.append(self.make_identifier())

            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MULTIPLY))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TT_DIVIDE))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()

            elif self.current_char == '=':
                tokens.append(Token(TT_EQ))
                self.advance()

            else:
                raise Exception(f"Illegal character '{self.current_char}'")

        tokens.append(Token(TT_EOF))
        return tokens


# =========================
# AST NODES
# =========================

class AST: pass


class NumberNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumberNode({self.value})"


class BinOpNode(AST):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op_token.type}, {self.right})"


class VarAccessNode(AST):
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"VarAccessNode({self.var_name_token.value})"


class VarAssignNode(AST):
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node

    def __repr__(self):
        return f"VarAssignNode({self.var_name_token.value}, {self.value_node})"


# =========================
# PARSER
# =========================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.idx += 1
        self.current_tok = self.tokens[self.idx] if self.idx < len(self.tokens) else None
        return self.current_tok

    def peek(self):
        nxt = self.idx + 1
        if nxt < len(self.tokens):
            return self.tokens[nxt]
        return None

    def parse(self):
        return self.expr()

    # ---------------------
    # GRAMMAR:
    # expr : IDENTIFIER '=' expr
    #      | term ((+|-) term)*
    #
    # term : factor ((*|/) factor)*
    #
    # factor : INTEGER
    #        | IDENTIFIER
    #        | LPAREN expr RPAREN
    # ---------------------

    def expr(self):

        # assignment has lowest precedence
        if self.current_tok.type == TT_IDENTIFIER:
            next_tok = self.peek()

            if next_tok is not None and next_tok.type == TT_EQ:
                var_name = self.current_tok
                self.advance()  # eat identifier
                self.advance()  # eat '='

                value_node = self.expr()
                return VarAssignNode(var_name, value_node)

        # otherwise arithmetic expression
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MULTIPLY, TT_DIVIDE))

    def factor(self):
        tok = self.current_tok

        if tok.type == TT_INTEGER:
            self.advance()
            return NumberNode(tok)

        elif tok.type == TT_IDENTIFIER:
            self.advance()
            return VarAccessNode(tok)

        elif tok.type == TT_LPAREN:
            self.advance()
            expr_node = self.expr()

            if self.current_tok.type != TT_RPAREN:
                raise Exception("Missing ')'")
            self.advance()

            return expr_node

        raise Exception("Invalid syntax")

    def bin_op(self, func, ops):
        left = func()

        while self.current_tok is not None and self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)

        return left


# =========================
# TEST DRIVER
# =========================

def run(text):
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()

    parser = Parser(tokens)
    ast = parser.parse()

    print(f"INPUT : {text}")
    print("TOKENS:", tokens)
    print("AST   :", ast)
    print("-" * 60)


# Demo tests
if __name__ == "__main__":

    # Access
    run("x")
    run("my_var")

    # Assignment
    run("x = 100")

    # Expression + Assign
    run("y = x + 5")

    # Valid arithmetic
    run("10 + 2 * (5 - 3)")
