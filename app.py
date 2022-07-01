from email.mime.text import MIMEText
import os
import smtplib
from flask import Flask, render_template, request, url_for, Response
from flask import *
from flask_mail import Mail
from formAbout import formString
from sendMail import formSendMail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

import pandas as pd
from bs4 import BeautifulSoup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_form.db'
db = SQLAlchemy(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(30), nullable=False)
    feeling = db.Column(db.String(10), nullable=False)
    what = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=True)
    about = db.Column(db.String(2000), nullable=True)
    post_time = db.Column(db.DATETIME, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

from_email = 'juvenic1950@gmail.com'
to_email = '1892jbr@gmail.com'
to_email2 = 'howlingliverpool@gmail.com'
account = 'juvenic1950@gmail.com'
password = 'rwiveyxnxxxhtawc'

app.config['NAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_NAME'] = 'juvenic@outlook.jp'
app.config['MAIL_USER_PASSWORD'] = 'rwiveyxnxxxhtawc'

mail = Mail(app)

class SearchForm(FlaskForm):
    feeling = SelectField('今の気分', coerce=int)
    what = SelectField('何について', coerce=int)
    year = SelectField('学年', coerce=int)
    start_date = DateField('検索開始日', format="%Y-%m-%d")
    end_date = DateField('検索終了日', format="%Y-%m-%d")
    submit = SubmitField('検索')

CSV_EXPORT = {
    'encoding': 'utf-8-sig',
}

@app.route("/")

def debug():
    msg = 'Copyright © 2022 Abukuma Education All Rights Reserved.'
    return msg

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/select_survey_students")
def select_survey_students():
    return render_template('select_survey_students.html')

@app.route("/select_survey_teacher")
def select_survey_teacher():
    return render_template('select_survey_teacher.html')

@app.route("/materials_contact")
def materials_contact():
    return render_template('materials_contact.html')

@app.route("/students")
def index_students():
    return render_template('students_index.html')

@app.route("/teacher")
def index_teacher():
    return render_template('teacher_index.html')

@app.route("/send")
def send():
    return render_template('send.html')

#数値化機能
@app.route("/graph")
def graph(forms):
    return render_template('preparation.html')

#集計機能
@app.route("/select", methods=['GET','POST'])
def select():

    forms = db.session.query(Form).filter_by(school="テスト小学校").all()

    url = request.url
    #request.url使ってスクレイピングしてCSV
    dfs = pd.read_html('https://juvenic.perma.jp/juvenic/select', encoding='utf-8')
    dfs[0].columns = ['学校名','今の気分','何について','学年','出席番号','相談内容','投稿時間']

    if request.method == "POST":
        if 'getcsv' in request.form:
            now = datetime.now().strftime('%Y%m%d%I:%M')
            title = "onayami"
            csvtitle = now + title

            response = Response(dfs[0].to_csv(index=False).encode('utf_8_sig'))
            response.headers["Content-type"] = "text/csv"
            response.headers['Content-Disposition'] = 'attachment; filename='+ csvtitle +'.csv'

            return response          

            #csvボタン押下時
        if 'tograph' in request.form:
            #数値化ボタン押下時
            return graph(forms=forms)
            #graph(forms)で遷移

    return render_template('select.html', forms=forms)

#フォーム機能
@app.route("/students_form_new", methods=['GET','POST'])
def students_form_new():
    if request.method == "POST":

        subject = '悩み相談：テスト小学校'
        schoolName = "テスト小学校"

        bodytext = formString(Form, db, schoolName)
        formSendMail(bodytext, account, password, subject, from_email, to_email, to_email2)
        return render_template('send.html', success=True)
    return render_template("students_form_new.html")

@app.route("/students_form", methods=['GET','POST'])
def submit():
    if request.method == "POST":

        subject = '悩み相談'

        name =  request.form.get('name')
        school = request.form.get('school')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学校：" + school + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

#小学校
@app.route("/students_form_misaka", methods=['GET','POST'])
def submit_misaka():
    if request.method == "POST":

        subject = '悩み相談：みさか小学校'
        schoolName = "みさか小学校"

        bodytext = formString(Form, db, schoolName)
        formSendMail(bodytext, account, password, subject, from_email, to_email, to_email2)
        return render_template('send.html', success=True)
    return render_template("students_form_new.html")

@app.route("/students_form_sekibe", methods=['GET','POST'])
def submit_sekibe():
    if request.method == "POST":

        subject = '悩み相談：関辺小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_kamako", methods=['GET','POST'])
def submit_kamako():
    if request.method == "POST":

        subject = '悩み相談：釜子小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_goka", methods=['GET','POST'])
def submit_goka():
    if request.method == "POST":

        subject = '悩み相談：五箇小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_kotagawa", methods=['GET','POST'])
def submit_kotagawa():
    if request.method == "POST":

        subject = '悩み相談：小田川小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_onoda", methods=['GET','POST'])
def submit_onoda():
    if request.method == "POST":

        subject = '悩み相談：小野田小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shinobu1", methods=['GET','POST'])
def submit_shinobu1():
    if request.method == "POST":

        subject = '悩み相談：信夫第一小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shinobu2", methods=['GET','POST'])
def submit_shinobu2():
    if request.method == "POST":

        subject = '悩み相談：信夫第二小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_ooya", methods=['GET','POST'])
def submit_ooya():
    if request.method == "POST":

        subject = '悩み相談：大屋小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shirakawa1", methods=['GET','POST'])
def submit_shirakawa1():
    if request.method == "POST":

        subject = '悩み相談：白河第一小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shirakawa2", methods=['GET','POST'])
def submit_shirakawa2():
    if request.method == "POST":

        subject = '悩み相談：白河第二小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shirakawa3", methods=['GET','POST'])
def submit_shirakawa3():
    if request.method == "POST":

        subject = '悩み相談：白河第三小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shirakawa4", methods=['GET','POST'])
def submit_shirakawa4():
    if request.method == "POST":

        subject = '悩み相談：白河第四小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_shirakawa5", methods=['GET','POST'])
def submit_shirakawa5():
    if request.method == "POST":

        subject = '悩み相談：白河第五小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_omotegou", methods=['GET','POST'])
def submit_omotegou():
    if request.method == "POST":

        subject = '悩み相談：表郷小学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

#中学校
@app.route("/students_form_jh_goka", methods=['GET','POST'])
def submit_jh_goka():
    if request.method == "POST":

        subject = '悩み相談：五箇中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_taishin", methods=['GET','POST'])
def submit_jh_taishin():
    if request.method == "POST":

        subject = '悩み相談：大信中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_chuou", methods=['GET','POST'])
def submit_jh_chuou():
    if request.method == "POST":

        subject = '悩み相談：中央中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_higashi", methods=['GET','POST'])
def submit_jh_higashi():
    if request.method == "POST":

        subject = '悩み相談：東中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_touhoku", methods=['GET','POST'])
def submit_jh_touhoku():
    if request.method == "POST":

        subject = '悩み相談：東北中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_minami", methods=['GET','POST'])
def submit_jh_minami():
    if request.method == "POST":

        subject = '悩み相談：南中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_shirakawa2", methods=['GET','POST'])
def submit_jh_shirakawa2():
    if request.method == "POST":

        subject = '悩み相談：白河第二中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_omotegou", methods=['GET','POST'])
def submit_jh_omotegou():
    if request.method == "POST":

        subject = '悩み相談：表郷中学校'

        name =  request.form.get('name')
        yaer = request.form.get('yaer')
        about = request.form.get('about')
        bodytext = "名前：" + name + "\n" + "学年：" + yaer + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

#西郷村_小学校
@app.route("/students_form_kumakura", methods=['GET','POST'])
def submit_kumakura():
    if request.method == "POST":

        subject = '悩み相談：熊倉小学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_yone", methods=['GET','POST'])
def submit_yone():
    if request.method == "POST":

        subject = '悩み相談：米小学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_odakura", methods=['GET','POST'])
def submit_odakura():
    if request.method == "POST":

        subject = '悩み相談：小田倉小学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_habuto", methods=['GET','POST'])
def submit_habuto():
    if request.method == "POST":

        subject = '悩み相談：羽太小学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

@app.route("/students_form_kawatani", methods=['GET','POST'])
def submit_kawatani():
    if request.method == "POST":

        subject = '悩み相談：川谷小学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form.html")

#西郷_中学校
@app.route("/students_form_jh_nishigou1", methods=['GET','POST'])
def submit_jh_nishigou1():
    if request.method == "POST":

        subject = '悩み相談：西郷第一中学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_nishigou2", methods=['GET','POST'])
def submit_jh_nishigou2():
    if request.method == "POST":

        subject = '悩み相談：西郷第二中学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

@app.route("/students_form_jh_kawatani", methods=['GET','POST'])
def submit_jh_kawatani():
    if request.method == "POST":

        subject = '悩み相談：川谷中学校'

        feeling =  request.form.get('feeling')
        what = request.form.get('what')
        year = request.form.get('year')
        name =  request.form.get('name')
        about = request.form.get('about')
        bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("students_form_jh.html")

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

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            
    return url_for(endpoint, **values)