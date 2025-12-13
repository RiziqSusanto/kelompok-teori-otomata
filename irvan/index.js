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
    "10 + 2 * (5 - 3)",
    "10 + * ",
];

targetCases.forEach((expression, index) => {
    console.log(`\nTest ${index + 1}: "${expression}"`);
    const result = Parser.validate(expression);

    if (result.valid) {
        console.log(`✅ Valid`);
    } else {
        console.log(`❌ Invalid `);
    }
});
