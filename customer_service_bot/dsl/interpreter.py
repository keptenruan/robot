#实现解释器，遍历AST并执行相应的操作。
class WhenNode:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

class LoopNode:
    def __init__(self, body):
        self.body = body

class Interpreter:
    def __init__(self, script):
        self.script = script
        self.token_stream = Lexer(script).tokenize()
        self.ast = Parser(self.token_stream).parse()

    def execute(self, user_input):
        for node in self.ast:
            if isinstance(node, WhenNode):
                if self.match_condition(node.condition, user_input):
                    self.perform_action(node.action)
            elif isinstance(node, LoopNode):
                while True:
                    for action in node.body:
                        if action.lower() == 'repeat':
                            self.perform_action(self.last_message)
                        else:
                            self.perform_action(action)
                    break

    def match_condition(self, condition, user_input):
        return user_input.strip().lower() == condition.strip().lower().strip('"')

    def perform_action(self, action):
        print(" ".join(action))
        self.last_message = action