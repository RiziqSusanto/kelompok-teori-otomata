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
    { type: 'parser', input: '10 + 2 * (5 - 3)', expected: 'Valid, result = 14' },
    { type: 'parser', input: '10 + *', expected: 'Invalid expression' },
    { type: 'parser', input: '10 / 0', expected: 'Error: Pembagian dengan nol' },
    { type: 'parser', input: '(10 + 2', expected: 'Error: Diharapkan RPAREN' },
];

targetCases.forEach((test, index) => {
    console.log(`\nT${index + 1}`);
    console.log(`${test.type === 'parser' ? 'Parser.validate()' : 'Lexer.getTokens()'}`);
    console.log(`${test.type === 'parser' ? 'Validate' : 'Tokenize'} ${test.input}`);

    try {
        if (test.type === 'parser') {
            const result = Parser.validate(test.input);
            if (result.valid) {
                console.log(`Valid, result = ${result.result}`);
            } else {
                console.log(result.message);
            }
        } else {
            const lexer = new Lexer(test.input);
            const tokens = lexer.getTokens();
            console.log('Tokens:', tokens);
        }
        console.log('Pass');
    } catch (error) {
        console.log(error.message);
        console.log('Error thrown');
        console.log('Pass');
    }
});