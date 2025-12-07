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


def print_tokens(tokens):
    """Pretty print token list"""
    print("-" * 40)
    print(f"{'No.':<5} {'Type':<12} {'Value':<10}")
    print("-" * 40)
    for i, token in enumerate(tokens, 1):
        value_str = repr(token.value) if token.value is not None else 'None'
        print(f"{i:<5} {token.type:<12} {value_str:<10}")
    print("-" * 40)


# MAIN - Testing Lexer
if __name__ == '__main__':
    # Test cases
    test_expressions = [
        "(10 + 2) * 5",           # Target dari soal
        "3 + 4 * 2",              # Tanpa kurung
        "100 / (25 - 5)",         # Angka besar
        "((1+2)*(3+4))",          # Nested parentheses
        "42",                      # Single number
    ]
    
    print("=" * 50)
    print("   Tugas Lexer")
    print("=" * 50)
    
    for expr in test_expressions:
        print(f"\nInput: \"{expr}\"")
        
        try:
            lexer = Lexer(expr)
            tokens = lexer.tokenize()
            print_tokens(tokens)
        except Exception as e:
            print(f"Error: {e}")
    
    # Interactive mode
    print("\n" + "=" * 50)
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
            
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            print_tokens(tokens)
            
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nBye!")
            break