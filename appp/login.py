from flask import render_template, flash, session, redirect, request
from app import db, models, app
from .forms import UserForm, CompleteForm
from werkzeug.security import generate_password_hash, check_password_hash
import json

@app.route('/ourstory', methods=['GET', 'POST'])
def ourstory():
    return render_template('ourstory.html')


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    data = json.loads(request.data)
    exists = 1; #indicates username doesnt already exist
    username = str(data.get('username'))
    if models.User.query.filter(models.User.username == username).count()>0:
        debug = models.Log(level="DEBUG", text="User exists already.")
        db.session.add(debug)
        db.session.commit()
        exists = 2 #indicates username already exists

    return json.dumps(exists)

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_form = UserForm()
    if user_form.validate_on_submit(): #submitted when validate succeeds
        debug = models.Log(level="DEBUG", text="User register credentials validated.")
        db.session.add(debug)
        db.session.commit()
        password_hash = generate_password_hash(user_form.password.data, method='pbkdf2:sha256', salt_length=6)
        user = models.User(username=user_form.username.data, password=password_hash)
        db.session.add(user)
        info = models.Log(level="INFO", text="New user added to database.")
        db.session.add(info)
        db.session.commit()
        return redirect("/")

    return render_template('register.html', form=user_form)

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('id'):
        session.pop('id') #logs users out when visiting login screen by popping their session id variable

    user_form = UserForm()
    formtwo = CompleteForm()
    if user_form.validate_on_submit():
        for p in models.User.query.filter(models.User.username == user_form.username.data): #get user by username
            if check_password_hash(p.password, user_form.password.data): #check password matches
                debug = models.Log(level="DEBUG", text="User login credentials validated.")
                db.session.add(debug)
                session["id"] = p.id
                info = models.Log(level="INFO", text="User logged in.")
                db.session.add(info)
                db.session.commit()
                return redirect("/profile")
                break

    return render_template('login.html',form=user_form, formtwo=formtwo)
