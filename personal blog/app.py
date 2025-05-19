from flask import Flask,render_template,request,url_for,redirect,session
import json
import time

app=Flask(__name__)
app.secret_key='secret_key'

user_credentials={
    "elpi":"elpiesjoto"
}

@app.route('/')
def home():
    with open('data.json',"r") as f:
        data = json.load(f)
    return render_template('home.html',data=data)

@app.route('/article_generator',methods=['POST'])
def article_generator():
    with open('data.json',"r") as file:
        data = json.load(file)
    article_id = request.form.get('id')
    for article in data:
        if article['id'] ==article_id:
            data_article = article
            break
    if not data:
        return render_template('article.html',error="Article not found")
    return render_template('article.html',data=data_article)

@app.route('/admin_login')
def login():
    return render_template('login.html')
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')  
        if username in user_credentials and user_credentials[username] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/admin',methods=['GET'])
def admin():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    with open('data.json',"r") as file:
        data = json.load(file)
    return render_template('admin.html',data=data)

@app.route('/admin',methods=['POST'])
def admin_delete():
    i=1
    data_article = []
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    with open('data.json',"r") as file:
        data = json.load(file)
    article_id = str(request.form.get('delete'))
    for article in data:
        if article['id'] !=article_id:
            article['id'] = str(i)
            i+=1
            data_article.append(article)
    with open('data.json', 'w') as file:
        json.dump(data_article, file)
    return redirect(url_for('admin'))

@app.route('/new_article',methods=["GET"])
def new_article():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    return render_template('new_article.html')

@app.route('/new_article/post',methods=["POST"])
def new_article_post():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    with open('data.json',"r") as file:
        data = json.load(file)
    title = request.form.get('title')
    content = request.form.get('content')
    new_article = {
        "id": str(len(data) + 1),
        "date": time.strftime("%Y-%m-%d"),
        "title": title,
        "content": content
    }
    data.append(new_article)
    with open('data.json', 'w') as file:
        json.dump(data, file)
    return redirect(url_for('admin'))


@app.route('/edit_article/<article_id>', methods=["GET", "POST"])
def edit_article(article_id):
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    with open('data.json', "r") as file:
        data = json.load(file)
    article = next((a for a in data if a['id'] == article_id), None)
    if not article:
        return "Artículo no encontrado", 404
    if request.method == "POST":
        article['title'] = request.form.get('title')
        article['content'] = request.form.get('content')
        with open('data.json', 'w') as file:
            json.dump(data, file)
        return redirect(url_for('admin'))
    return render_template('edit_article.html', article=article)

if __name__== '__main__':
    app.run('0.0.0.0',port=5000,debug=True)

