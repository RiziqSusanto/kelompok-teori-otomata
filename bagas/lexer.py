class TokenType:
    INTEGER = 'INTEGER'      # Angka: 0, 1, 10, 123, dll
    PLUS = 'PLUS'            # Operator: +
    MINUS = 'MINUS'          # Operator: -
    MULTIPLY = 'MULTIPLY'    # Operator: *
    DIVIDE = 'DIVIDE'        # Operator: /
    LPAREN = 'LPAREN'        # (
    RPAREN = 'RPAREN'        # )
    EOF = 'EOF'              # End of File


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos] if text else None

    def advance(self):
        """Pindah ke karakter berikutnya."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Lewati spasi."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Baca angka integer multidigit."""
        num = ""
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return int(num)

    def get_next_token(self):
        """Lexer utama: mengembalikan token satu per satu."""
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


# --- Contoh penggunaan ---
lexer = Lexer("(10 + 2) * 5")
tokens = []

while True:
    token = lexer.get_next_token()
    tokens.append(token)
    if token.type == TokenType.EOF:
        break

print(tokens)
