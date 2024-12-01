from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .db.config import Config
from .db.models import db
from .db.db_utils import init_db

def create_app():
    """
    创建并配置 Flask 应用实例。
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 在这里调用 init_db 并传递 app 参数
    with app.app_context():
        init_db(app)
    
    # 启用 CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # 注册蓝图
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# 添加这个部分以支持直接运行 run.py
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)