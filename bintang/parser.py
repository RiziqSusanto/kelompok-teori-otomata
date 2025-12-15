# --- Kelas Error ---
class SyntaxError(Exception):
    """Kelas untuk error sintaksis yang lebih informatif."""
    def __init__(self, token, expected):
        # Asumsikan token memiliki posisi untuk info lebih lanjut
        pos = token.pos if hasattr(token, 'pos') else '?'
        message = f"Syntax Error: Unexpected token '{token.value}' ({token.type}) at pos {pos}. Expected: {expected}."
        super().__init__(message)

# --- Definisi Tipe Token (Lanjutan dari sebelumnya) ---
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
        self.pos = pos # Menambahkan posisi untuk error handling yang lebih baik

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# --- Kelas Lexer (Disesuaikan dengan penambahan posisi) ---
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
            if self.current_char.isspace():
                self.advance()

            elif self.current_char.isdigit():
                tokens.append(self.make_number())

            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, value='+', pos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, value='-', pos=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, value='*', pos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, value='/', pos=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, value='(', pos=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, value=')', pos=self.pos))
                self.advance()

            else:
                raise Exception(f"Illegal Character: '{self.current_char}' at pos {self.pos}")

        # Tambahkan token akhir opsional (EOF) untuk mempermudah parser,
        # meskipun tidak wajib untuk parser validasi sederhana ini.
        return tokens

    def make_number(self):
        num_str = ''
        start_pos = self.pos # Simpan posisi awal angka

        while self.current_char != None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()

        return Token(TT_INT, int(num_str), pos=start_pos)


# --- Kelas Parser ---
class Parser:
    """
    Kelas yang bertanggung jawab membangun struktur pohon (AST) dan memvalidasi sintaks.
    Untuk saat ini hanya melakukan validasi sintaks.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        """Memajukan kursor ke token berikutnya."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        """Fungsi utama, memanggil aturan grammar tertinggi (expr)."""
        if self.current_token is None:
            # Input kosong dianggap valid (atau bisa kita buat tidak valid)
            return "Valid (Input Kosong)"

            # Panggil aturan grammar tertinggi (Expression)
        self.parse_expr()

        # Setelah parsing selesai, harusnya tidak ada token sisa (kecuali EOF)
        if self.current_token is None:
            return "Valid"
        else:
            # Jika masih ada token tersisa, berarti ada yang salah
            raise SyntaxError(self.current_token, "end of input")

    def parse_eat(self, token_type, expected_msg):
        """
        Helper untuk memastikan token saat ini sesuai harapan, lalu maju (eat)
        Jika tidak sesuai, lempar SyntaxError.
        """
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            # Current token adalah token yang salah
            raise SyntaxError(self.current_token if self.current_token else Token("EOF", value="<End>", pos=self.pos), expected_msg)


    # --- Aturan Grammar (Recursive Descent) ---

    # factor : INT | LPAREN expr RPAREN
    def parse_factor(self):
        token = self.current_token

        if token and token.type == TT_INT:
            self.parse_eat(TT_INT, "INT")
            # Dalam parser AST sungguhan, kita akan mengembalikan node angka di sini

        elif token and token.type == TT_LPAREN:
            self.parse_eat(TT_LPAREN, "'('") # 'makan' (

            # Panggil aturan grammar yang lebih tinggi (Rekursif)
            self.parse_expr()

            self.parse_eat(TT_RPAREN, "')'") # harus diikuti oleh )

        else:
            # Jika bukan INT atau LPAREN, itu adalah Syntax Error
            raise SyntaxError(token if token else Token("EOF", value="<End>", pos=self.pos), "INT atau '('")


    # term : factor ((MUL | DIV) factor)*
    def parse_term(self):
        # 1. Selalu mulai dengan memanggil aturan dengan prioritas yang lebih tinggi (Factor)
        self.parse_factor()

        # 2. Loop untuk menangani operator * dan /
        while self.current_token and self.current_token.type in (TT_MUL, TT_DIV):
            op_token = self.current_token

            # 'Makan' operator * atau /
            self.parse_eat(op_token.type, f"'{op_token.value}'")

            # Harus diikuti oleh Factor lain (mempertahankan loop)
            self.parse_factor()


    # expr : term ((PLUS | MINUS) term)*
    def parse_expr(self):
        # 1. Selalu mulai dengan memanggil aturan dengan prioritas yang lebih tinggi (Term)
        self.parse_term()

        # 2. Loop untuk menangani operator + dan -
        while self.current_token and self.current_token.type in (TT_PLUS, TT_MINUS):
            op_token = self.current_token

            # 'Makan' operator + atau -
            self.parse_eat(op_token.type, f"'{op_token.value}'")

            # Harus diikuti oleh Term lain (mempertahankan loop)
            self.parse_term()


# --- Fungsi Utama untuk menjalankan Lexer dan Parser ---
def run_validation(text):
    print(f"\n--- Memproses Input: \"{text}\" ---")

    # Tahap 1: Lexical Analysis
    try:
        lexer = Lexer(text)
        tokens = lexer.make_tokens()
        print(f"Token: {tokens}")
    except Exception as e:
        print(f"❌ Lexer Error: {e}")
        return "Invalid"

    # Tahap 2: Parsing (Sintaks Analysis)
    try:
        parser = Parser(tokens)
        result = parser.parse()
        print(f"Result: {result}")
        return "Valid"
    except SyntaxError as e:
        print(f"❌ Parser Error: {e}")
        return "Invalid"


# --- Contoh Penggunaan dan Target Validasi ---

# Test Kasus 1: Valid
run_validation("10 + 2 * (5 - 3)")

# Test Kasus 2: Invalid (Syntax Error)
run_validation("10 + * ")

# Test Kasus 3: Invalid (Kurung tidak seimbang)
run_validation("(1 + 2")

# Test Kasus 4: Valid
run_validation("4 / 2 - 1")