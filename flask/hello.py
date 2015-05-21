#/usr/bin/python
#Filename: hello.py

from flask import Flask,session,redirect,url_for,escape,request,abort
from flask import render_template
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s'% escape(session['username'])
    return 'You are not logged in!'
    # return redirect(url_for('login'))
    # return 'Index Page'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')
    # return '''
    #     <form action='' method="post">
    #         <p><input type=text name=username>
    #         <p><input type=submit value=Login>
    #     </form>
    # '''
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

app.secret_key = '\xa3\xfa\xe7wKC\xd6\xf98\x82"e\xe3Z\xe8\xf4\xf3\x10m\xe4M&\x15V'


@app.route('/hello/')
def hello():
    return "hello world"

@app.route('/user/<username>')
def show_user_profile(username):
    return username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return post_id

@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello2(name=None):
    return render_template('hello.html',name=name)

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f=request.files['the_file']
        f.save('static/a.txt')




if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
