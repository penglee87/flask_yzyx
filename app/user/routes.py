from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.user import bp
from app.models import Article
from app import db

# 创建文章路由
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
        
        new_article = Article(title=title, content=content, category=category, user_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        
        flash('文章创建成功')
        return redirect(url_for('question.article', article_id=new_article.id))
    
    return render_template('user/create_article.html')

# 用户个人中心
@bp.route('/profile')
@login_required
def profile():
    user_articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.created_at.desc()).all()
    return render_template('user/profile.html', articles=user_articles)