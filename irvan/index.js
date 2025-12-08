// Implementasikan Lexer sederhana yang mampu membaca:

// - Operasi Aritmatika : +, -, *, /
// - Tanda kurung ( , )
// - Integer (Angka multi-digit)
// - Mengabaikan spasi

import { Lexer } from './lexer.js';

// Target → (10 + 2 ) * 5 → Output Token List
const input = "(10 + 2 ) * 5";

const lexer = new Lexer(input);

const tokens = lexer.getTokens();
console.log(tokens);
