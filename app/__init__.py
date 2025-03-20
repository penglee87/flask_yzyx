from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config

# 初始化扩展，但不绑定到应用实例
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

def create_app(config_class=Config):
    # 创建应用实例
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    from app.question import bp as question_bp
    app.register_blueprint(question_bp, url_prefix='/question')
    
    # 确保实例文件夹存在
    from pathlib import Path
    Path(app.instance_path).mkdir(exist_ok=True)
    
    return app