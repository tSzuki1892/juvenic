from email.message import Message
from email.mime.text import MIMEText
import os
import smtplib
from flask import Flask, render_template, request
from sympy import re
from flask_mail import Mail, Message



app = Flask(__name__)

app.config['NAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USER_NAME'] = '1892jbr@gmail.com'
app.config['MAIL_USER_PASSWORD'] = 'lyon1950'

mail = Mail(app)

@app.route("/")

def debug():
    msg = 'Copyright © 2022 Abukuma Education All Rights Reserved.'
    return msg

@app.route("/students")
def index_students():
    return render_template('students_index.html')


@app.route("/teacher")

def index_teacher():
    return render_template('teacher_index.html')

@app.route("/form", methods=['GET','POST'])

def form():
    if request.method == "POST":
        name = request.form.get('name')
        school = request.form.get('school')
        yaer = request.form.get('yaer')
        about = request.form.get('about')

        msg = Message('Hello', sender='1892jbr@gmail.com', recipients = ['1892jbr@gmail.com'])
        msg.body = name,school,yaer,about
        mail.send(msg)
        return render_template("form.html", success=True)
    return render_template("form.html")

@app.route("/submit", methods=['GET','POST'])

def submit():

    account = "1892jbr@gmail.com"
    password = "lyon1950"

    to_email = "1892jbr@gmail.com"
    from_email = "howlingliverpool@gmail.com"

    subject = "test mail"
    message = "test mail"
    msg = MIMEText(message, "html")
    msg["name"] = request.form.get('name')
    msg["school"] = request.form.get('school')
    msg["yaer"] = request.form.get('yaer')
    msg["about"] = request.form.get('about')

    message = "送信されました！相談して頂きありがとうございます<m(__)m>"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(account, password)
    server.sendmail(msg)
    server.quit()
    return render_template('form.html')

#request利用の場合
@app.route('/next')
def index_post():
    if request.method == 'GET':
        name = request.args['name']
    elif request.method == 'POST':
        name = request.form['name']
    response = render_template('next.hrml',
    title='送信完了ページ',
    name=name)

    return response

#デバッグ用CSS変更反映コード
@app.context_processor
def add_staticfile():
    def staticfile_cp(fname):
        path = os.path.join(app.root_path, 'static/css', fname)
        mtime =  str(int(os.stat(path).st_mtime))
        return '/static/css/' + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)

#ファビコン設定
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")