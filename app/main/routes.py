from flask import render_template, request, redirect, url_for, flash
from app.main import bp
from app.models import Article, FinancialNews

# 首页路由
@bp.route('/')
def index():
    articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
    news = FinancialNews.query.order_by(FinancialNews.published_at.desc()).limit(10).all()
    return render_template('index.html', articles=articles, news=news)

# 财经资讯路由
@bp.route('/financial_news')
def financial_news():
    news = FinancialNews.query.order_by(FinancialNews.published_at.desc()).all()
    return render_template('financial_news.html', news=news)

# 财经资讯详情路由
@bp.route('/news/<int:news_id>')
def news_detail(news_id):
    news = FinancialNews.query.get_or_404(news_id)
    return render_template('news_detail.html', news=news)