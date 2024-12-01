from flask import Blueprint, request, jsonify
from .scripts.script_parser import parse_script

# 定义一个蓝图
main = Blueprint('main', __name__)

@main.route('/execute', methods=['POST'])
def execute_script():
    """
    处理执行脚本的请求。
    """
    data = request.get_json()
    script = data.get('script')
    if not script:
        return jsonify({"error": "Script is required."}), 400

    responses = parse_script(script)
    return jsonify({"responses": responses})