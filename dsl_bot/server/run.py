import os
import sys

# 将项目根目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)