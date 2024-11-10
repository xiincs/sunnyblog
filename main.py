import json

from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '1211lmx'
app.template_folder = 'templates'
app.config['STATIC_FOLDER'] = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1211lmx@localhost:3307/db001'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open('blog.config.json', 'r') as f:
    config = json.load(f)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    is_logged_in = 'logged_in' in session
    articles = Article.query.all()
    return render_template('index.html', articles=articles, is_logged_in=is_logged_in, **config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    is_logged_in = 'logged_in' in session
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', is_logged_in=is_logged_in, **config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    is_logged_in = 'logged_in' in session
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify(status="Invalid username or password.")
        session['logged_in'] = True
        session['username'] = username
        return jsonify(status="success")  # 登录成功
    if is_logged_in:
        return redirect(url_for('index'))
    return render_template('login.html', status="", is_logged_in=is_logged_in, **config)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit_article', methods=['GET', 'POST'])
def edit_article():
    is_logged_in = 'logged_in' in session
    if 'logged_in' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_article = Article(title=title, content=content)
            db.session.add(new_article)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit_article.html',is_logged_in=is_logged_in,  **config)
    else:
        return render_template('login.html', status="",is_logged_in=is_logged_in, **config)

@app.route('/read_article/<int:article_id>', methods=['GET', 'POST'])
def read_article(article_id):
    is_logged_in = 'logged_in' in session
    if 'logged_in' in session:
        article = Article.query.filter_by(id=article_id).first()
        if article:
            return render_template('read_article.html', is_logged_in=is_logged_in, article=article, **config)
    else:
        return render_template('login.html', status="", is_logged_in=is_logged_in,  **config)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)