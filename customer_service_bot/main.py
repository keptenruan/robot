# 项目的主入口点，负责初始化解释器、加载DSL脚本并启动交互式会话。
from dsl.interpreter import Interpreter
from scripts import basic_script, order_status, account_details

def load_script(script_path):
    with open(script_path, 'r') as file:
        return file.read()

def main():
    scripts = {
        'basic': load_script('scripts/basic_script.dsl'),
        'order_status': load_script('scripts/order_status.dsl'),
        'account_details': load_script('scripts/account_details.dsl')
    }

    interpreter = Interpreter(scripts['basic'])
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        interpreter.execute(user_input)

if __name__ == '__main__':
    main()