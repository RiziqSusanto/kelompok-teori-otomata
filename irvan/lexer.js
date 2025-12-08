const TOKEN = {
    INT: "INT",
    PLUS: "PLUS",
    MINUS: "MINUS",
    MUL: "MUL",
    DIV: "DIV",
    LPAREN: "LPAREN",
    RPAREN: "RPAREN"
};

export class Lexer {
    constructor(text) {
        this.text = text;
        this.pos = 0;
        this.currentChar = this.text[this.pos] || null;
    }

    advance() {
        this.pos++;
        this.currentChar = this.pos < this.text.length
            ? this.text[this.pos]
            : null;
    }

    skipWhitespace() {
        while (this.currentChar !== null && /\s/.test(this.currentChar)) {
            this.advance();
        }
    }

    integer() {
        let result = "";
        while (this.currentChar !== null && /[0-9]/.test(this.currentChar)) {
            result += this.currentChar;
            this.advance();
        }
        return parseInt(result, 10);
    }

    getTokens() {
        const tokens = [];

        while (this.currentChar !== null) {

            if (/\s/.test(this.currentChar)) {
                this.skipWhitespace();
                continue;
            }

            if (/[0-9]/.test(this.currentChar)) {
                tokens.push({ type: TOKEN.INT, value: this.integer() });
                continue;
            }

            if (this.currentChar === "+") {
                tokens.push({ type: TOKEN.PLUS, value: "+" });
                this.advance();
                continue;
            }

            if (this.currentChar === "-") {
                tokens.push({ type: TOKEN.MINUS, value: "-" });
                this.advance();
                continue;
            }

            if (this.currentChar === "*") {
                tokens.push({ type: TOKEN.MUL, value: "*" });
                this.advance();
                continue;
            }

            if (this.currentChar === "/") {
                tokens.push({ type: TOKEN.DIV, value: "/" });
                this.advance();
                continue;
            }

            if (this.currentChar === "(") {
                tokens.push({ type: TOKEN.LPAREN, value: "(" });
                this.advance();
                continue;
            }

            if (this.currentChar === ")") {
                tokens.push({ type: TOKEN.RPAREN, value: ")" });
                this.advance();
                continue;
            }

            throw new Error(`Karakter tidak valid: ${this.currentChar}`);
        }

        return tokens;
    }
}

