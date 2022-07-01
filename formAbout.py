from flask import request
from formDb import insertFormDb


def formString(Form, db, schoolName):
    feeling =  request.form.get('feeling')
    what = request.form.get('what')
    year = request.form.get('year')
    number = request.form.get('number')
    if number == None:
        number = 0
    name =  request.form.get('name')
    about = request.form.get('about')

    insertFormDb(feeling, schoolName, what, year, number, name, about, Form, db)

    bodytext = "気分：" + feeling + "\n" + "どんなこと：" + what + "\n" + "名前：" + name + "\n" + "学年：" + year + "\n" + "相談：" + about
    return bodytext