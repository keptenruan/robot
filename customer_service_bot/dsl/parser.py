# 实现语法分析器，将标记流转换为抽象语法树（AST）。
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            token_type, token_value = self.tokens[self.pos]
            if token_type == 'WHEN':
                condition = self.parse_condition()
                action = self.parse_action()
                ast.append(WhenNode(condition, action))
            elif token_type == 'LOOP':
                loop_body = self.parse_loop()
                ast.append(LoopNode(loop_body))
            self.pos += 1
        return ast

    def parse_condition(self):
        self.consume('WHEN')
        condition = self.consume('STRING')
        self.consume('THEN')
        return condition

    def parse_action(self):
        action = []
        while self.peek()[0] != 'END':
            action.append(self.consume('STRING'))
        self.consume('END')
        return action

    def parse_loop(self):
        self.consume('LOOP')
        body = []
        while self.peek()[0] != 'END':
            body.append(self.consume('STRING'))
        self.consume('END')
        return body

    def consume(self, expected_type):
        token_type, token_value = self.tokens[self.pos]
        if token_type == expected_type:
            self.pos += 1
            return token_value
        else:
            raise SyntaxError(f"Expected {expected_type}, but got {token_type}")

    def peek(self):
        return self.tokens[self.pos]