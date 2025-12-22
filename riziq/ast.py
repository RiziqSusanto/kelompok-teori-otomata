# Definisi tipe-tipe token
class TokenType:
    INTEGER = 'INTEGER'      # Angka: 0, 1, 10, 123, dll
    PLUS = 'PLUS'            # Operator: +
    MINUS = 'MINUS'          # Operator: -
    MULTIPLY = 'MULTIPLY'    # Operator: *
    DIVIDE = 'DIVIDE'        # Operator: /
    LPAREN = 'LPAREN'        # Tanda kurung buka: (
    RPAREN = 'RPAREN'        # Tanda kurung tutup: )
    EOF = 'EOF'              # End of File/Input


class Token:
    """Representasi sebuah token"""
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


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
            
            # --- INTEGER (angka multi-digit) ---
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            
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
    def __init__(self, value):
        self.value = value

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


# ============================================
# PARSER
# ============================================

class Parser:
    """
    Recursive Descent Parser untuk grammar aritmatika:

    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | LPAREN expr RPAREN
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected=None):
        """Raise exception untuk syntax error"""
        if expected:
            raise Exception(f'Parser Error: Diharapkan {expected}, tetapi dapat {self.current_token.type}')
        raise Exception(f'Parser Error: Syntax tidak valid pada token {self.current_token}')

    def eat(self, token_type):
        """
        Consume token saat ini jika sesuai dengan tipe yang diharapkan
        Jika tidak sesuai, raise error
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self):
        """
        factor : INTEGER | LPAREN expr RPAREN
        Return: NumberNode atau hasil dari expr (dalam kurung)
        """
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return NumberNode(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        else:
            self.error('INTEGER atau LPAREN')

    def term(self):
        """
        term : factor ((MULTIPLY | DIVIDE) factor)*
        Return: Node (NumberNode atau BinOpNode)
        """
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                op = '*'
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                op = '/'

            right = self.factor()
            node = BinOpNode(op, node, right)

        return node

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        Return: Node (NumberNode atau BinOpNode)
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                op = '+'
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
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
        if self.current_token.type != TokenType.EOF:
            self.error('EOF (end of input)')

        return ast


def validate_expression(text):
    """
    Fungsi helper untuk validasi ekspresi
    Return: (is_valid, message)
    """
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        parser.parse()
        return True, "✅ Valid"
    except Exception as e:
        return False, f"❌ Invalid: {e}"


def print_tokens(tokens):
    """Pretty print token list"""
    print("-" * 40)
    print(f"{'No.':<5} {'Type':<12} {'Value':<10}")
    print("-" * 40)
    for i, token in enumerate(tokens, 1):
        value_str = repr(token.value) if token.value is not None else 'None'
        print(f"{i:<5} {token.type:<12} {value_str:<10}")
    print("-" * 40)


# MAIN - Testing Lexer & Parser
if __name__ == '__main__':
    # ==========================================
    # TEST PARSER - Validasi Grammar
    # ==========================================
    print("=" * 50)
    print("   Tugas Parser - Validasi Grammar")
    print("=" * 50)
    print("\nGrammar:")
    print("  expr   : term ((PLUS | MINUS) term)*")
    print("  term   : factor ((MUL | DIV) factor)*")
    print("  factor : INT | LPAREN expr RPAREN")
    print("-" * 50)

    # Test cases untuk parser
    parser_test_cases = [
        # Valid expressions
        ("10 + 2 * (5 - 3)", True),
        ("(10 + 2) * 5", True),
        ("3 + 4 * 2", True),
        ("100 / (25 - 5)", True),
        ("((1+2)*(3+4))", True),
        ("42", True),
        # Invalid expressions
        ("10 + * ", False),
        ("+ 5", False),
        ("(10 + 2", False),
        ("10 + 2)", False),
        ("", False),
        ("10 +", False),
    ]

    print("\n📋 Hasil Validasi Parser:\n")
    for expr, expected_valid in parser_test_cases:
        is_valid, message = validate_expression(expr)
        status = "PASS" if is_valid == expected_valid else "FAIL"
        print(f'  "{expr}"')
        print(f'     → {message} [{status}]\n')

    # ==========================================
    # TEST LEXER - Tokenisasi
    # ==========================================
    print("\n" + "=" * 50)
    print("   Tugas Lexer - Tokenisasi")
    print("=" * 50)

    lexer_test_expressions = [
        "(10 + 2) * 5",
        "10 + 2 * (5 - 3)",
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
    # TEST AST - Abstract Syntax Tree
    # ==========================================
    print("\n" + "=" * 50)
    print("   Tugas AST - Abstract Syntax Tree")
    print("=" * 50)

    ast_test_expressions = [
        "3 * (4 + 5)",
        "10 + 2 * 5",
        "42",
        "(1 + 2) * (3 + 4)",
    ]

    for expr in ast_test_expressions:
        print(f"\nInput: \"{expr}\"")
        print("-" * 40)
        try:
            lexer = Lexer(expr)
            parser = Parser(lexer)
            ast = parser.parse()
            print(ast)
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