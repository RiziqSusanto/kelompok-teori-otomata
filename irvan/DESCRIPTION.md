# Laporan Perancangan Parser Sederhana

## Pendahuluan

Parser sederhana ini dirancang untuk mengevaluasi ekspresi matematika dasar yang meliputi operasi aritmatika (+, -, *, /), tanda kurung, dan bilangan bulat Parser menggunakan pendekatan recursive descent parsing dengan precedence yang tepat: perkalian dan pembagian memiliki prioritas lebih tinggi daripada penjumlahan dan pengurangan

## Perancangan Lexer
Lexer bertugas untuk melakukan tokenisasi input string menjadi token-token yang dapat dipahami oleh parser Lexer ini mengenali:
- Bilangan bulat (multi-digit)
- Operator: +, -, *, /
- Tanda kurung: (, )
- Mengabaikan spasi

### Fungsi dalam Lexer

1. constructor(text): Inisialisasi lexer dengan input text, posisi awal 0, dan karakter saat ini
2. advance(): Memajukan posisi ke karakter berikutnya dan mengupdate currentChar
3. skipWhitespace(): Melewati karakter spasi hingga menemukan karakter non-spasi
4. integer(): Mengumpulkan digit-digit untuk membentuk bilangan bulat dan mengembalikan nilai integer
5. getTokens(): Loop utama yang memproses setiap karakter:
   - Jika spasi, skip
   - Jika digit, parse integer
   - Jika operator atau tanda kurung, buat token sesuai
   - Jika karakter tidak valid, throw error

### Proses Pengecekan Lexer

Lexer memproses input karakter per karakter Untuk setiap karakter:
- Cek apakah spasi: skip
- Cek apakah digit: mulai parse integer
- Cek apakah operator atau tanda kurung: buat token dan advance
- Jika tidak cocok, error

Contoh: Input "(10 + 2 ) * 5"
- Token: LPAREN, INT(10), PLUS, INT(2), RPAREN, MUL, INT(5)

## Perancangan Parser

Parser menggunakan metode recursive descent untuk mengurai ekspresi dengan grammar:
- expr: term ((PLUS | MINUS) term)*
- term: factor ((MUL | DIV) factor)*
- factor: INT | LPAREN expr RPAREN

### Fungsi dalam Parser

1. constructor(input): Buat lexer, dapatkan tokens, tambah EOF token
2. error(message): Throw error dengan pesan
3. eat(tokenType): Konsumsi token jika cocok, advance ke token berikutnya
4. factor(): Parse faktor: integer atau (expr)
5. term(): Parse term: factor dengan * atau /
6. expr(): Parse ekspresi: term dengan + atau -
7. parse(): Mulai parsing dari expr, cek EOF, return hasil atau error
8. static validate(input): Method statis untuk validasi ekspresi

### Proses Pengecekan Parser

Parser mengikuti grammar:
- expr() memanggil term(), lalu loop untuk + atau -
- term() memanggil factor(), lalu loop untuk * atau /
- factor() cek INT atau LPAREN, jika LPAREN rekursif ke expr()

Pengecekan error: Jika token tidak cocok, throw error 