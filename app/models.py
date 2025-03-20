from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)  # 允许为空，微信登录用户可能没有密码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    articles = db.relationship('Article', backref='author', lazy=True)
    role = db.Column(db.String(20), default='user')  # 用户角色：admin或user
    
    # 微信登录相关字段
    wechat_openid = db.Column(db.String(100), unique=True, nullable=True)
    wechat_unionid = db.Column(db.String(100), unique=True, nullable=True)
    wechat_nickname = db.Column(db.String(100), nullable=True)
    wechat_avatar = db.Column(db.String(500), nullable=True)
    login_type = db.Column(db.String(20), default='normal')  # normal, wechat
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_admin(self):
        return self.role == 'admin'

# 文章模型
class Article(db.Model):
    __tablename__ = 't_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  # 主图片URL（保留向后兼容）
    comments = db.relationship('Comment', backref='article', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('ArticleImage', backref='article', lazy=True, cascade='all, delete-orphan')
    
# 文章图片模型
class ArticleImage(db.Model):
    __tablename__ = 't_article_image'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500), nullable=False)  # 图片URL
    article_id = db.Column(db.Integer, db.ForeignKey('t_article.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# 财经资讯模型
# 评论模型
class Comment(db.Model):
    __tablename__ = 't_comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('t_article.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('t_comment.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
# 财经资讯模型
class FinancialNews(db.Model):
    __tablename__ = 't_financial_news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))