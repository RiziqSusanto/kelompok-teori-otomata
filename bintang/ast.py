# --- Definisi Tipe Token ---
TT_INT    = 'INT'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_MUL    = 'MUL'
TT_DIV    = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

# --- Kelas Token ---
class Token:
    def __init__(self, type_, value=None, pos=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value is not None else f'{self.type}'

# ==========================================
# 1. DESAIN NODE AST [cite: 232]
# ==========================================

class AST:
    pass

class NumberNode(AST):
    """Menyimpan angka (Leaf node) [cite: 234]"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumberNode({self.value})"

class BinOpNode(AST):
    """Operasi biner (+, -, *, /) yang punya sisi kiri dan kanan [cite: 235]"""
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

    def __repr__(self):
        # Format string agar menghasilkan output nested seperti di slide
        return f"BinOpNode({self.op_token.value},\n  {self.left},\n  {self.right}\n)"

# --- Kelas Lexer (Tetap sama seperti sebelumnya) ---
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char.isspace(): self.advance()
            elif self.current_char.isdigit(): tokens.append(self.make_number())
            elif self.current_char == '+': tokens.append(Token(TT_PLUS, '+', self.pos)); self.advance()
            elif self.current_char == '-': tokens.append(Token(TT_MINUS, '-', self.pos)); self.advance()
            elif self.current_char == '*': tokens.append(Token(TT_MUL, '*', self.pos)); self.advance()
            elif self.current_char == '/': tokens.append(Token(TT_DIV, '/', self.pos)); self.advance()
            elif self.current_char == '(': tokens.append(Token(TT_LPAREN, '(', self.pos)); self.advance()
            elif self.current_char == ')': tokens.append(Token(TT_RPAREN, ')', self.pos)); self.advance()
            else: raise Exception(f"Illegal Character: '{self.current_char}'")
        return tokens

    def make_number(self):
        num_str = ''; start_pos = self.pos
        while self.current_char != None and self.current_char.isdigit():
            num_str += self.current_char; self.advance()
        return Token(TT_INT, int(num_str), pos=start_pos)

# ==========================================
# 2. MODIFIKASI PARSER UNTUK AST [cite: 237]
# ==========================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Syntax Error: Expected {token_type}")

    def parse(self):
        """Mulai membangun pohon dari aturan tertinggi [cite: 181]"""
        return self.expr()

    def factor(self):
        """factor : INT | LPAREN expr RPAREN [cite: 238]"""
        token = self.current_token

        if token.type == TT_INT:
            self.eat(TT_INT)
            return NumberNode(token) # Return node, bukan None [cite: 239]

        elif token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expr() # Rekursif ke expr
            self.eat(TT_RPAREN)
            return node # Kurung dibuang (Abstract), hanya return isinya [cite: 221]

    def term(self):
        """term : factor ((MUL | DIV) factor)* [cite: 240]"""
        node = self.factor() # Node kiri [cite: 242]

        while self.current_token and self.current_token.type in (TT_MUL, TT_DIV):
            token = self.current_token
            self.eat(token.type)
            # Bangun node secara bertahap (node lama jadi anak kiri) [cite: 242]
            node = BinOpNode(left=node, op_token=token, right=self.factor())

        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)* [cite: 241]"""
        node = self.term() # Node kiri

        while self.current_token and self.current_token.type in (TT_PLUS, TT_MINUS):
            token = self.current_token
            self.eat(token.type)
            # Bangun BinOpNode baru [cite: 242]
            node = BinOpNode(left=node, op_token=token, right=self.term())

        return node

# ==========================================
# 3. RUN & TARGET OUTPUT [cite: 245]
# ==========================================

def run_ast(text):
    print(f"Input: \"{text}\"")
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast_root = parser.parse()
    print("-" * 20)
    print(ast_root)

# Target Tugas: 3 * (4 + 5)
run_ast("3 * (4 + 5)")