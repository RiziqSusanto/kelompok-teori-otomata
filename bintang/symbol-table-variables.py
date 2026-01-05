import string

# Konstanta Token
TT_MINUS  = 'MINUS'    # Operator -
TT_DIV    = 'DIV'      # Operator /
TT_LPAREN = 'LPAREN'   # Tanda kurung buka (
TT_RPAREN = 'RPAREN'   # Tanda kurung tutup )

TT_INT        = 'INT'
TT_FLOAT      = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER' # [cite: 33]
TT_EQ         = 'EQ'         # [cite: 34]
TT_PLUS       = 'PLUS'
TT_MUL        = 'MUL'

# Karakter yang diizinkan untuk Identifier
LETTERS = string.ascii_letters
DIGITS = '0123456789'
LETTERS_DIGITS = LETTERS + DIGITS

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

# Di dalam class Lexer, tambahkan logika untuk membuat identifier:
# (Asumsi: self.current_char adalah karakter saat ini)
def make_identifier(self):
    id_str = ''
    while self.current_char != None and self.current_char in LETTERS_DIGITS:
        id_str += self.current_char
        self.advance()
    return Token(TT_IDENTIFIER, id_str)

class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token # Menyimpan token identifier

class VarAssignNode:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token # Nama variabel [cite: 37, 42]
        self.value_node = value_node           # Expression di kanan '=' [cite: 38, 42]

class Parser:
    # ... (method __init__ dan advance) ...

    def atom(self):
        token = self.current_token

        if token.type == TT_IDENTIFIER:
            self.advance()
            return VarAccessNode(token) # Case 2: Expression/Access

        # ... (logika untuk NumberNode, dll) ...

    def expr(self):
        # Logika Lookahead untuk Assignment
        if self.current_token.type == TT_IDENTIFIER:
            # Cek apakah token berikutnya adalah EQUALS
            # Ini memerlukan fungsi peek() atau pengecekan manual
            var_name = self.current_token
            self.advance()

            if self.current_token.type == TT_EQ:
                self.advance()
                value = self.expr() # Rekursif mengambil nilai di kanan '='
                return VarAssignNode(var_name, value) # Case 1: Assignment
            else:
                # Jika bukan '=', maka ini adalah akses variabel biasa
                # Kita harus mengembalikan state atau menangani sebagai AccessNode
                return VarAccessNode(var_name)


# --- Kelas Token ---
class Token:
    """
    Kelas untuk merepresentasikan unit terkecil yang bermakna (Token).
    """
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    # Representasi string untuk mempermudah pencetakan (debugging/output)
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# --- Kelas Lexer ---
class Lexer:
    """
    Kelas yang bertanggung jawab untuk mengubah teks mentah menjadi daftar Token.
    """
    def __init__(self, text):
        self.text = text
        self.pos = -1         # Posisi kursor saat ini [cite: 82]
        self.current_char = None # Karakter yang ditunjuk kursor [cite: 83]
        self.advance()

    def advance(self):
        """
        Memajukan kursor ke karakter berikutnya dan memperbarui current_char.
        Jika sudah di akhir teks, current_char diatur menjadi None. [cite: 84]
        """
        self.pos += 1
        # Mengambil karakter, jika index di luar batas, atur None
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        """
        Fungsi utama untuk menghasilkan daftar token dari teks input.
        """
        tokens = []

        # Loop selama masih ada karakter yang harus diproses
        while self.current_char != None:
            # 1. Mengabaikan Spasi (Whitespace)
            if self.current_char.isspace():
                self.advance()

            # 2. Membaca Angka Multi-Digit [cite: 85, 88, 117]
            elif self.current_char.isdigit():
                tokens.append(self.make_number())

            # 3. Membaca Operator dan Kurung
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()

            # 4. Penanganan Karakter Ilegal (Error Handling) [cite: 106, 108]
            else:
                # Untuk bahasa sederhana, kita bisa mengasumsikan karakter lain adalah ilegal
                char = self.current_char
                self.advance()
                raise Exception(f"Illegal Character: '{char}'")

        return tokens

    def make_number(self):
        """
        Membaca dan mengembalikan Token INT multi-digit. [cite: 88]
        """
        num_str = ''

        # Terus berjalan selama kursor menunjuk ke digit
        while self.current_char != None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance() # Majukan kursor

        # Setelah loop selesai, num_str berisi seluruh angka (misal: "10" atau "123")
        # Konversi ke integer dan buat Token
        return Token(TT_INT, int(num_str))

# --- Contoh Penggunaan ---
def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    return tokens

# Target input: (10 + 2 ) * 5 [cite: 119]
input_text = "(10 + 2 ) * 5"

print(f"Input Teks: \"{input_text}\"")
try:
    result_tokens = run(input_text)
    print("\n✅ Output Token List:")
    print(result_tokens)
except Exception as e:
    print(f"\n❌ Error saat Lexing: {e}")