import { Lexer } from './lexer.js';

const TOKEN = {
    INT: "INT",
    PLUS: "PLUS",
    MINUS: "MINUS",
    MUL: "MUL",
    DIV: "DIV",
    LPAREN: "LPAREN",
    RPAREN: "RPAREN",
    EOF: "EOF"
};

class NumberNode {
    constructor(value) {
        this.value = value;
    }

    toString() {
        return `NumberNode(${this.value})`;
    }
}

class BinOpNode {
    constructor(op, left, right) {
        this.op = op;
        this.left = left;
        this.right = right;
    }

    toString(indent = 0) {
        const pad = ' '.repeat(indent);
        return `BinOpNode(${this.op},\n${pad}  ${this.left.toString(indent + 2)},\n${pad}  ${this.right.toString(indent + 2)})`;
    }
}

export class Parser {
    constructor(input) {
        this.lexer = new Lexer(input);
        this.tokens = this.lexer.getTokens();
        this.tokens.push({ type: TOKEN.EOF, value: null });
        this.pos = 0;
        this.currentToken = this.tokens[this.pos];
    }

    error() {
        throw new Error(`Invalid`);
    }

    eat(tokenType) {
        if (this.currentToken.type === tokenType) {
            this.pos++;
            this.currentToken = this.tokens[this.pos];
        } else {
            this.error(`Diharapkan ${tokenType}, tapi mendapat ${this.currentToken.type}`);
        }
    }

    factor() {
        const token = this.currentToken;

        if (token.type === TOKEN.INT) {
            this.eat(TOKEN.INT);
            return new NumberNode(token.value);
        } else if (token.type === TOKEN.LPAREN) {
            this.eat(TOKEN.LPAREN);
            const result = this.expr();
            this.eat(TOKEN.RPAREN);
            return result;
        } else {
            this.error("Diharapkan integer atau ekspresi dalam kurung");
        }
    }

    term() {
        let result = this.factor();

        while (this.currentToken.type === TOKEN.MUL || this.currentToken.type === TOKEN.DIV) {
            const token = this.currentToken;
            if (token.type === TOKEN.MUL) {
                this.eat(TOKEN.MUL);
                result = new BinOpNode('*', result, this.factor());
            } else if (token.type === TOKEN.DIV) {
                this.eat(TOKEN.DIV);
                result = new BinOpNode('/', result, this.factor());
            }
        }

        return result;
    }

    expr() {
        let result = this.term();

        while (this.currentToken.type === TOKEN.PLUS || this.currentToken.type === TOKEN.MINUS) {
            const token = this.currentToken;
            if (token.type === TOKEN.PLUS) {
                this.eat(TOKEN.PLUS);
                result = new BinOpNode('+', result, this.term());
            } else if (token.type === TOKEN.MINUS) {
                this.eat(TOKEN.MINUS);
                result = new BinOpNode('-', result, this.term());
            }
        }

        return result;
    }

    parse() {
        try {
            const result = this.expr();

            if (this.currentToken.type !== TOKEN.EOF) {
                this.error("Token tak terduga setelah ekspresi selesai");
            }

            return {
                valid: true,
                result: result,
                message: "Ekspresi valid"
            };
        } catch (error) {
            return {
                valid: false,
                result: null,
                message: error.message
            };
        }
    }

    static validate(input) {
        const parser = new Parser(input);
        return parser.parse();
    }
}
