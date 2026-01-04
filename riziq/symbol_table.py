import string

# Definisi tipe-tipe token
class TokenType:
    INTEGER = 'INTEGER'        # Angka: 0, 1, 10, 123, dll
    PLUS = 'PLUS'              # Operator: +
    MINUS = 'MINUS'            # Operator: -
    MULTIPLY = 'MULTIPLY'      # Operator: *
    DIVIDE = 'DIVIDE'          # Operator: /
    LPAREN = 'LPAREN'          # Tanda kurung buka: (
    RPAREN = 'RPAREN'          # Tanda kurung tutup: )
    EOF = 'EOF'                # End of File/Input
    IDENTIFIER = 'IDENTIFIER'  # Nama variabel: x, y, result, dll
    KEYWORD = 'KEYWORD'        # Kata kunci: var, if, else, dll
    EQ = 'EQ'                  # Operator assignment: =

# Karakter yang diperbolehkan untuk nama variabel
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + string.digits + '_'

# Daftar kata kunci
KEYWORDS = ['var', 'if', 'else', 'while', 'for']


class Token:
    """Representasi sebuah token"""
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


# ============================================
# LEXER
# ============================================

class Lexer:
    """
    Lexical Analyzer (Scanner)
    Mengubah string input menjadi sequence of tokens
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0  # Posisi karakter saat ini
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, char):
        """Raise exception untuk karakter tidak valid"""
        raise Exception(f'Lexer Error: Karakter tidak valid "{char}" pada posisi {self.pos}')

    def advance(self):
        """Maju ke karakter berikutnya dalam input"""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None  # End of input

    def skip_whitespace(self):
        """Lewati semua whitespace (spasi, tab, newline)"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """
        Baca sequence digit dan kembalikan sebagai integer
        Mendukung angka multi-digit (10, 123, 9999, dll)
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def make_identifier(self):
        """
        Baca identifier atau keyword
        Logika:
        1. Loop selama karakter adalah huruf/angka/_
        2. Gabungkan menjadi satu string
        3. Cek apakah string tersebut ada di list KEYWORDS
        4. Jika ada -> Return Token KEYWORD
        5. Jika tidak -> Return Token IDENTIFIER
        """
        id_str = ''

        # Loop selama karakter adalah huruf/angka/_
        while self.current_char is not None and self.current_char in LETTERS_DIGITS:
            id_str += self.current_char
            self.advance()

        # Cek apakah ini keyword?
        tok_type = TokenType.KEYWORD if id_str in KEYWORDS else TokenType.IDENTIFIER

        return Token(tok_type, id_str)

    def get_next_token(self):
        """
        Tokenizer utama
        Memecah input menjadi token satu per satu
        """
        while self.current_char is not None:

            # --- Abaikan whitespace ---
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # --- IDENTIFIER atau KEYWORD ---
            if self.current_char in LETTERS:
                return self.make_identifier()

            # --- INTEGER (angka multi-digit) ---
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            # --- OPERATOR ASSIGNMENT ---
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQ, '=')

            # --- OPERATOR ARITMATIKA ---
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

            # --- TANDA KURUNG ---
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            # --- KARAKTER TIDAK DIKENAL ---
            self.error(self.current_char)

        # End of input
        return Token(TokenType.EOF, None)

    def tokenize(self):
        """
        Menghasilkan list semua token dari input
        Return: List[Token]
        """
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)  # Tambahkan token EOF
        return tokens


# ============================================
# AST NODE CLASSES
# ============================================

class NumberNode:
    """Node untuk merepresentasikan angka dalam AST"""
    def __init__(self, tok):
        self.tok = tok
        self.value = tok.value

    def __repr__(self):
        return f'NumberNode({self.value})'


class BinOpNode:
    """Node untuk merepresentasikan operasi biner dalam AST"""
    def __init__(self, op, left, right):
        self.op = op        # Operator: +, -, *, /
        self.left = left    # Node kiri
        self.right = right  # Node kanan

    def __repr__(self):
        return self._repr_indent(0)

    def _repr_indent(self, indent):
        """Helper untuk pretty print dengan indentasi"""
        spaces = '  ' * indent

        # Format left node
        if isinstance(self.left, BinOpNode):
            left_str = self.left._repr_indent(indent + 1)
        else:
            left_str = '  ' * (indent + 1) + repr(self.left)

        # Format right node
        if isinstance(self.right, BinOpNode):
            right_str = self.right._repr_indent(indent + 1)
        else:
            right_str = '  ' * (indent + 1) + repr(self.right)

        return f'{spaces}BinOpNode({self.op},\n{left_str},\n{right_str}\n{spaces})'


class VarAccessNode:
    """
    Node untuk mengakses nilai variabel
    Contoh: dalam ekspresi "a + 5", "a" adalah VarAccessNode
    """
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

    def __repr__(self):
        return f'VarAccessNode({self.var_name_tok.value})'


class VarAssignNode:
    """
    Node untuk assignment variabel
    Contoh: "x = 10" menghasilkan VarAssignNode(x, NumberNode(10))
    """
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

    def __repr__(self):
        return self._repr_indent(0)

    def _repr_indent(self, indent):
        """Helper untuk pretty print dengan indentasi"""
        spaces = '  ' * indent

        # Format value node
        if isinstance(self.value_node, BinOpNode):
            value_str = self.value_node._repr_indent(indent + 1)
        elif isinstance(self.value_node, VarAssignNode):
            value_str = self.value_node._repr_indent(indent + 1)
        else:
            value_str = '  ' * (indent + 1) + repr(self.value_node)

        return f'{spaces}VarAssignNode({self.var_name_tok.value},\n{value_str}\n{spaces})'


# ============================================
# PARSER
# ============================================

class Parser:
    """
    Recursive Descent Parser untuk grammar aritmatika dengan variabel:

    expr   : IDENTIFIER EQ expr | term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | IDENTIFIER | LPAREN expr RPAREN
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        """Maju ke token berikutnya"""
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        else:
            # Ambil token baru dari lexer
            self.current_tok = self.lexer.get_next_token()
            self.tokens.append(self.current_tok)
        return self.current_tok

    def peek(self):
        """
        Mengintip token selanjutnya tanpa memajukan posisi
        Digunakan untuk lookahead dalam parsing
        """
        peek_idx = self.tok_idx + 1
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        else:
            # Ambil token baru dari lexer dan simpan
            next_tok = self.lexer.get_next_token()
            self.tokens.append(next_tok)
            return next_tok

    def error(self, expected=None):
        """Raise exception untuk syntax error"""
        if expected:
            raise Exception(f'Parser Error: Diharapkan {expected}, tetapi dapat {self.current_tok.type}')
        raise Exception(f'Parser Error: Syntax tidak valid pada token {self.current_tok}')

    def factor(self):
        """
        factor : INTEGER | IDENTIFIER | LPAREN expr RPAREN
        Return: NumberNode, VarAccessNode, atau hasil dari expr (dalam kurung)
        """
        tok = self.current_tok

        if tok.type == TokenType.INTEGER:
            self.advance()
            return NumberNode(tok)

        # TAMBAHAN BARU: Handle Identifier
        elif tok.type == TokenType.IDENTIFIER:
            self.advance()
            return VarAccessNode(tok)

        elif tok.type == TokenType.LPAREN:
            self.advance()
            node = self.expr()
            if self.current_tok.type != TokenType.RPAREN:
                self.error('RPAREN')
            self.advance()
            return node

        else:
            self.error('INTEGER, IDENTIFIER, atau LPAREN')

    def term(self):
        """
        term : factor ((MULTIPLY | DIVIDE) factor)*
        Return: Node (NumberNode, VarAccessNode, atau BinOpNode)
        """
        node = self.factor()

        while self.current_tok.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            tok = self.current_tok
            if tok.type == TokenType.MULTIPLY:
                self.advance()
                op = '*'
            elif tok.type == TokenType.DIVIDE:
                self.advance()
                op = '/'

            right = self.factor()
            node = BinOpNode(op, node, right)

        return node

    def expr(self):
        """
        expr : IDENTIFIER EQ expr | term ((PLUS | MINUS) term)*

        Logika lookahead:
        1. Cek apakah token sekarang adalah IDENTIFIER
        2. Cek apakah token NEXT adalah '='
        3. Jika YA: ini adalah assignment
        4. Jika TIDAK: ini adalah expression biasa
        """
        # Cek Assignment: Var = Expr
        if self.current_tok.type == TokenType.IDENTIFIER:
            next_tok = self.peek()  # Lihat ke depan

            if next_tok.type == TokenType.EQ:
                var_name = self.current_tok
                self.advance()  # makan IDENTIFIER
                self.advance()  # makan '='
                val = self.expr()  # parse nilai di sebelah kanan
                return VarAssignNode(var_name, val)

        # Jika bukan assignment, jalankan logic biasa (Binary Operation)
        node = self.term()

        while self.current_tok.type in (TokenType.PLUS, TokenType.MINUS):
            tok = self.current_tok
            if tok.type == TokenType.PLUS:
                self.advance()
                op = '+'
            elif tok.type == TokenType.MINUS:
                self.advance()
                op = '-'

            right = self.term()
            node = BinOpNode(op, node, right)

        return node

    def parse(self):
        """
        Entry point parser - membangun AST
        Return: AST (Node) jika valid, raise Exception jika tidak valid
        """
        ast = self.expr()

        # Pastikan semua input telah dikonsumsi
        if self.current_tok.type != TokenType.EOF:
            self.error('EOF (end of input)')

        return ast


# ============================================
# HELPER FUNCTIONS
# ============================================

def validate_expression(text):
    """
    Fungsi helper untuk validasi ekspresi
    Return: (is_valid, message)
    """
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        parser.parse()
        return True, "Valid"
    except Exception as e:
        return False, f"Invalid: {e}"


def print_tokens(tokens):
    """Pretty print token list"""
    print("-" * 40)
    print(f"{'No.':<5} {'Type':<12} {'Value':<10}")
    print("-" * 40)
    for i, token in enumerate(tokens, 1):
        value_str = repr(token.value) if token.value is not None else 'None'
        print(f"{i:<5} {token.type:<12} {value_str:<10}")
    print("-" * 40)


# ============================================
# MAIN - Testing
# ============================================

if __name__ == '__main__':
    # ==========================================
    # TEST LEXER - Tokenisasi dengan Identifier
    # ==========================================
    print("=" * 50)
    print("   Tugas Symbol Table & Variables")
    print("=" * 50)

    print("\n" + "=" * 50)
    print("   TEST 1: Lexer - Tokenisasi Identifier")
    print("=" * 50)

    lexer_test_expressions = [
        "x",
        "my_var",
        "x = 10",
        "result = x + y",
    ]

    for expr in lexer_test_expressions:
        print(f"\nInput: \"{expr}\"")
        try:
            lexer = Lexer(expr)
            tokens = lexer.tokenize()
            print_tokens(tokens)
        except Exception as e:
            print(f"Error: {e}")

    # ==========================================
    # TEST PARSER - AST dengan Variabel
    # ==========================================
    print("\n" + "=" * 50)
    print("   TEST 2: Parser - AST dengan Variabel")
    print("=" * 50)

    # Test 1: Access
    print("\n--- Test 1: Access ---")
    print("Input: 'x' atau 'my_var'")
    print("Harus return VarAccessNode")
    for expr in ["x", "my_var"]:
        print(f"\nInput: \"{expr}\"")
        try:
            lexer = Lexer(expr)
            parser = Parser(lexer)
            ast = parser.parse()
            print(f"AST: {ast}")
        except Exception as e:
            print(f"Error: {e}")

    # Test 2: Assign
    print("\n--- Test 2: Assign ---")
    print("Input: 'x = 100'")
    print("Harus return VarAssignNode(x, 100)")
    expr = "x = 100"
    print(f"\nInput: \"{expr}\"")
    try:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        print(f"AST:\n{ast}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Complex
    print("\n--- Test 3: Complex ---")
    print("Input: 'y = x + 5'")
    print("AssignNode yang value-nya BinOpNode")
    expr = "y = x + 5"
    print(f"\nInput: \"{expr}\"")
    try:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        print(f"AST:\n{ast}")
    except Exception as e:
        print(f"Error: {e}")

    # ==========================================
    # TEST 3 
    # ==========================================
    print("\n" + "=" * 50)
    print("   TEST 3")
    print("=" * 50)
    print("\nInput yang diharapkan:")
    print("  x = 10")
    print("  y = 5")
    print("  result = x + y")
    print("\nOutput yang diharapkan:")
    print("  VarAssignNode(x, 10)")
    print("  VarAssignNode(y, 5)")
    print("  VarAssignNode(result, BinOpNode(VarAccessNode(x), PLUS, VarAccessNode(y)))")

    test_expressions = [
        "x = 10",
        "y = 5",
        "result = x + y",
    ]

    print("\n--- Hasil Parsing ---")
    for expr in test_expressions:
        print(f"\nInput: \"{expr}\"")
        try:
            lexer = Lexer(expr)
            parser = Parser(lexer)
            ast = parser.parse()
            print(f"AST:\n{ast}")
        except Exception as e:
            print(f"Error: {e}")

    # ==========================================
    # INTERACTIVE MODE
    # ==========================================
    print("\n" + "=" * 50)
    print("   Mode Interaktif")
    print("   Ketik 'exit' untuk keluar")
    print("=" * 50)

    while True:
        try:
            text = input("\nMasukkan ekspresi: ")
            if text.lower() == 'exit':
                print("Bye!")
                break
            if not text.strip():
                continue

            # Tokenisasi
            print("\nTokens:")
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            print_tokens(tokens)

            # Validasi dan AST
            print("Validasi:")
            is_valid, message = validate_expression(text)
            print(f"   {message}")

            # Tampilkan AST jika valid
            if is_valid:
                print("\nAST (Abstract Syntax Tree):")
                print("-" * 40)
                lexer = Lexer(text)
                parser = Parser(lexer)
                ast = parser.parse()
                print(ast)

        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nBye!")
            break
