import { Lexer } from './lexer.js';

const TOKEN = {
    INT: "INT",
    PLUS: "PLUS",
    MINUS: "MINUS",
    MUL: "MUL",
    DIV: "DIV",
    LPAREN: "LPAREN",
    RPAREN: "RPAREN",
    IDENTIFIER: "IDENTIFIER",
    KEYWORD: "KEYWORD",
    EQ: "EQ",
    EOF: "EOF"
};

class NumberNode {
    constructor(value) {
        this.value = value;
    }

    toString() {
        return `${this.value}`;
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
        return `BinOpNode(\n${pad}  ${this.left.toString(indent + 2)},\n${pad}  ${this.op},\n${pad}  ${this.right.toString(indent + 2)})`;
    }
}

class VarAccessNode {
    constructor(var_name_token) {
        this.var_name_token = var_name_token;
    }

    toString() {
        return `VarAccessNode(${this.var_name_token.value})`;
    }
}

class VarAssignNode {
    constructor(var_name_token, value_node) {
        this.var_name_token = var_name_token;
        this.value_node = value_node;
    }

    toString(indent = 0) {
        const pad = ' '.repeat(indent);
        return `VarAssignNode(${this.var_name_token.value}, ${this.value_node.toString(indent + 2)})`;
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
        } else if (token.type === TOKEN.IDENTIFIER) {
            this.eat(TOKEN.IDENTIFIER);
            return new VarAccessNode(token);
        } else if (token.type === TOKEN.LPAREN) {
            this.eat(TOKEN.LPAREN);
            const result = this.expr();
            this.eat(TOKEN.RPAREN);
            return result;
        } else {
            this.error("Diharapkan integer, identifier, atau ekspresi dalam kurung");
        }
    }

    term() {
        let result = this.factor();

        while (this.currentToken.type === TOKEN.MUL || this.currentToken.type === TOKEN.DIV) {
            const token = this.currentToken;
            if (token.type === TOKEN.MUL) {
                this.eat(TOKEN.MUL);
                result = new BinOpNode(token.type, result, this.factor());
            } else if (token.type === TOKEN.DIV) {
                this.eat(TOKEN.DIV);
                result = new BinOpNode(token.type, result, this.factor());
            }
        }

        return result;
    }

    bin_op_expr() {
        let result = this.term();

        while (this.currentToken.type === TOKEN.PLUS || this.currentToken.type === TOKEN.MINUS) {
            const token = this.currentToken;
            if (token.type === TOKEN.PLUS) {
                this.eat(TOKEN.PLUS);
                result = new BinOpNode(token.type, result, this.term());
            } else if (token.type === TOKEN.MINUS) {
                this.eat(TOKEN.MINUS);
                result = new BinOpNode(token.type, result, this.term());
            }
        }

        return result;
    }

    expr() {
        if (this.currentToken.type === TOKEN.IDENTIFIER && this.tokens[this.pos + 1] && this.tokens[this.pos + 1].type === TOKEN.EQ) {
            const var_name = this.currentToken;
            this.eat(TOKEN.IDENTIFIER);
            this.eat(TOKEN.EQ);
            const value = this.expr();
            return new VarAssignNode(var_name, value);
        } else {
            return this.bin_op_expr();
        }
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
