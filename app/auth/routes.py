from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required
from app.auth import bp
from app.models import User
from app import db
import uuid
import time

# 用户注册路由
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 检查用户名或邮箱是否已存在
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if user_exists:
            flash('用户名或邮箱已被注册')
            return redirect(url_for('auth.register'))
        
        # 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

# 用户登录路由
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
    
    return render_template('auth/login.html')

# 用户登出路由
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 微信登录路由
@bp.route('/wechat-login')
def wechat_login():
    # 这里只是一个简单的实现，实际项目中需要接入微信开放平台
    # 生成一个唯一的登录状态码，用于后续验证
    login_state = str(uuid.uuid4())
    
    # 在实际项目中，这里应该将login_state存储到数据库或缓存中
    # 并设置过期时间，用于后续验证微信扫码登录
    
    return render_template('auth/wechat_login.html', login_state=login_state)

# 微信登录状态检查API
@bp.route('/check-wechat-login/<login_state>')
def check_wechat_login(login_state):
    # 在实际项目中，这里应该查询数据库或缓存，检查login_state是否已被微信登录授权
    # 这里仅作为示例，模拟登录过程需要较长时间
    
    # 模拟检查登录状态的逻辑
    # 实际项目中，这里应该是检查数据库中该login_state是否已经被微信登录授权
    current_time = int(time.time())
    
    # 修改为只有在特定条件下才返回成功，大幅降低成功概率，延长等待时间
    # 这里设置为只有当时间戳是60的倍数时才返回成功（平均需要等待30秒）
    if current_time % 60 == 0:
        # 模拟登录成功
        # 在实际项目中，这里应该创建用户或查找已有用户，然后执行登录操作
        return jsonify({
            'status': 'success',
            'message': '登录成功'
        })
    else:
        # 模拟等待中
        return jsonify({
            'status': 'waiting',
            'message': '等待扫码'
        })

# 微信登录测试页面路由
@bp.route('/wechat-test')
def wechat_test():
    return render_template('auth/wechat_test.html')

# 微信授权回调路由
@bp.route('/wechat-auth')
def wechat_auth():
    # 获取state参数，这是我们之前生成的登录状态码
    login_state = request.args.get('state')
    
    if not login_state:
        return '无效的请求', 400
    
    # 在实际项目中，这里应该验证login_state是否有效
    # 然后执行微信授权登录的逻辑
    
    # 这里仅作为示例，返回一个简单的成功页面，并添加JavaScript代码通知原页面登录成功
    return '''
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>微信授权成功</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success-icon { font-size: 48px; color: #07C160; margin-bottom: 20px; }
            .message { font-size: 18px; margin-bottom: 30px; }
        </style>
        <script>
            // 将登录状态存储到localStorage中，以便网页端检测到登录成功
            document.addEventListener('DOMContentLoaded', function() {
                // 从URL中获取state参数
                const urlParams = new URLSearchParams(window.location.search);
                const state = urlParams.get('state');
                
                if (state) {
                    // 设置登录成功标志
                    localStorage.setItem('wechat_login_success_' + state, 'true');
                    
                    // 显示成功消息
                    document.getElementById('stateValue').textContent = state;
                }
            });
        </script>
    </head>
    <body>
        <div class="success-icon">✓</div>
        <div class="message">授权成功，请返回应用继续操作</div>
        <div style="font-size: 12px; color: #999; margin-top: 20px;">
            状态码: <span id="stateValue">-</span>
        </div>
    </body>
    </html>
    '''