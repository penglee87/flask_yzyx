from app import create_app, db
from app.models import User, Article, FinancialNews
from app import migrate

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Article': Article, 'FinancialNews': FinancialNews}

@app.cli.command('init-db')
def init_db():
    with app.app_context():  # 添加上下文
        db.create_all()
    print('数据库初始化完成')

@app.cli.command('seed-data')
def seed_data():
    # 添加测试用户
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)
    
    # 添加测试文章
    if Article.query.count() == 0:
        categories = ['投资策略', '基金分析', '股票研究', '财经知识']
        for i in range(10):
            article = Article(
                title=f'测试文章 {i+1}',
                content=f'这是测试文章 {i+1} 的内容，包含了一些财经知识和投资建议...',
                category=categories[i % len(categories)],
                user_id=1
            )
            db.session.add(article)
    
    # 添加测试财经资讯
    if FinancialNews.query.count() == 0:
        for i in range(10):
            news = FinancialNews(
                title=f'财经资讯 {i+1}',
                content=f'这是财经资讯 {i+1} 的详细内容，报道了最新的市场动态...',
                source='财经网',
                image_url='/static/images/news-placeholder.jpg'
            )
            db.session.add(news)
    
    db.session.commit()
    print('测试数据添加完成')

# 应用现在通过flask命令运行
# 环境变量在.flaskenv文件中配置