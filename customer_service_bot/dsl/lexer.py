#实现词法分析器，将DSL源代码转换为标记流（tokens）
import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        rules = [
            ('WHEN', r'when'),
            ('THEN', r'then'),
            ('END', r'end'),
            ('LOOP', r'loop'),
            ('STRING', r'"[^"]*"'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('WHITESPACE', r'\s+'),
            ('NEWLINE', r'\n'),
            ('INVALID', r'.')
        ]
        token_pattern = '|'.join('(?P<%s>%s)' % pair for pair in rules)
        for mo in re.finditer(token_pattern, self.text):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'WHITESPACE':
                continue
            elif kind == 'INVALID':
                raise RuntimeError(f'Unexpected character: {value}')
            self.tokens.append((kind, value))
        return self.tokens