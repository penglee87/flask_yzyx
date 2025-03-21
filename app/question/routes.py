from flask import render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import current_user, login_required
from app.question import bp
from app.models import Article, Comment, User
from app import db
import os
from werkzeug.utils import secure_filename
import uuid

# 文章列表路由
@bp.route('/articles')
def articles():
    category = request.args.get('category')
    if category:
        articles = Article.query.filter_by(category=category).order_by(Article.created_at.desc()).all()
    else:
        articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('question/articles.html', articles=articles, category=category)

# 文章详情路由
@bp.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # 处理评论提交
    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form.get('content')
        parent_id = request.form.get('parent_id')
        
        if content:
            comment = Comment(content=content, user_id=current_user.id, article_id=article_id)
            
            # 如果是回复评论，设置parent_id
            if parent_id:
                comment.parent_id = int(parent_id)
                flash('回复发布成功')
            else:
                flash('评论发布成功')
                
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('question.article', article_id=article_id))
    
    # 获取文章评论（只获取顶级评论，不包括回复）
    comments = Comment.query.filter_by(article_id=article_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    return render_template('question/article_detail.html', article=article, comments=comments)

# 管理员删除文章路由
@bp.route('/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # 检查是否为管理员
    if not current_user.is_admin():
        flash('只有管理员才能删除文章')
        return redirect(url_for('question.articles'))
    
    article = Article.query.get_or_404(article_id)
    
    # 删除文章（级联删除相关评论）
    db.session.delete(article)
    db.session.commit()
    
    flash('文章已成功删除')
    return redirect(url_for('question.articles'))

# 允许的图片文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 管理员创建文章路由
@bp.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    # 检查是否为管理员
    if not current_user.is_admin():
        flash('只有管理员才能创建文章')
        return redirect(url_for('question.articles'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        image = request.files.get('image')
        
        image_url = None
        if image and allowed_file(image.filename):
            # 生成安全的文件名
            filename = secure_filename(image.filename)
            # 添加唯一标识符，避免文件名冲突
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            # 确保上传目录存在
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            # 保存文件
            image_path = os.path.join(upload_folder, unique_filename)
            image.save(image_path)
            # 设置图片URL（相对路径，用于在模板中显示）
            image_url = f"uploads/{unique_filename}"
        
        if title and content and category:
            # 富文本内容已经包含了图片，直接保存
            article = Article(title=title, content=content, category=category, user_id=current_user.id, image_url=image_url)
            db.session.add(article)
            db.session.commit()
            flash('文章创建成功')
            return redirect(url_for('question.article', article_id=article.id))
    
    return render_template('question/create_article.html')

# 管理员编辑文章路由
@bp.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # 检查是否为管理员
    if not current_user.is_admin():
        flash('只有管理员才能编辑文章')
        return redirect(url_for('question.articles'))
    
    article = Article.query.get_or_404(article_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        image = request.files.get('image')
        
        if image and image.filename and allowed_file(image.filename):
            # 生成安全的文件名
            filename = secure_filename(image.filename)
            # 添加唯一标识符，避免文件名冲突
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            # 确保上传目录存在
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            # 保存文件
            image_path = os.path.join(upload_folder, unique_filename)
            image.save(image_path)
            # 设置图片URL（相对路径，用于在模板中显示）
            article.image_url = f"uploads/{unique_filename}"
        
        if title and content and category:
            article.title = title
            article.content = content
            article.category = category
            db.session.commit()
            flash('文章更新成功')
            return redirect(url_for('question.article', article_id=article.id))
    
    return render_template('question/edit_article.html', article=article)