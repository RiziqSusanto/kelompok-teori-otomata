// Implementasikan Lexer sederhana yang mampu membaca:

// - Operasi Aritmatika : +, -, *, /
// - Tanda kurung ( , )
// - Integer (Angka multi-digit)
// - Mengabaikan spasi

import { Lexer } from './lexer.js';
import { Parser } from './parser.js';

console.log("=== PENGUJIAN LEXER ===");
const input = "(10 + 2 ) * 5";

const lexer = new Lexer(input);

const tokens = lexer.getTokens();
console.log(`Input: ${input}`);
console.log("Token list:", tokens);

console.log("\n=== PENGUJIAN PARSER ===");

const targetCases = [
    "x = 100",
    "y = 5",
    "result = x + y"
];

targetCases.forEach((expression, index) => {
    console.log(`\nTest ${index + 1}: "${expression}"`);
    const result = Parser.validate(expression);

    if (result.valid) {
        console.log("Output:");
        console.log(result.result.toString());
    } else {
        console.log(`❌ Invalid `);
    }
});
