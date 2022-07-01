def insertFormDb(feeling, schoolName, what, year, number, name, about, Form, db):

    form = Form(feeling=feeling, school=schoolName, what=what, year=year, number=number, name=name, about=about)
    db.session.add(form)
    db.session.commit()
