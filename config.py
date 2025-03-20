import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'yzyx.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 每页显示的问题数量
    QUESTIONS_PER_PAGE = 10
    
    # 上传文件配置
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    
    # 微信开放平台配置
    WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID') or 'WECHAT_APP_ID'
    WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET') or 'WECHAT_APP_SECRET'
    WECHAT_REDIRECT_URI = os.environ.get('WECHAT_REDIRECT_URI') or 'http://localhost:5000/auth/wechat/callback'