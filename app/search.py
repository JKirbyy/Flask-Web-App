from flask import render_template, flash, session, redirect, request
from app import db, models, app
from .forms import SearchForm
import json


@app.route('/search/<ID>', methods=['GET', 'POST'])
def user(ID):
    if session.get('id'):
        search_form = SearchForm()
        if search_form.validate_on_submit(): #search for new user
            session["search"] = search_form.search.data
            return redirect("/search")
        user = models.User.query.get(ID)
        posts = user.stories #get users stories to display
        info = models.Log(level="INFO", text="User page visited.")
        db.session.add(info)
        db.session.commit()

        return render_template('otheruser.html', blog=posts, user=user, searchform=search_form)
    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')

@app.route('/follow', methods=['GET', 'POST']) #called when user requests authorship
def follow():
    debug = models.Log(level="DEBUG", text="Requested called.")
    db.session.add(debug)
    data = json.loads(request.data)
    requesting_user = int(data.get('requesting_user'))
    requested_story = int(data.get('requested_story'))
    r = models.Requests() #create a new requests object and set their user and story fields
    user = models.User.query.get(requesting_user)
    story = models.Story.query.get(requested_story)
    r.user = user
    r.story = story
    db.session.add(r)
    info = models.Log(level="INFO", text="Authorship requested.")
    db.session.add(info)
    db.session.commit()


    return json.dumps({'status': 'OK', 'response': 'response'})

@app.route('/search', methods=['GET', 'POST'])
def search():

    if session.get('id'):
        search_form = SearchForm()

        if search_form.validate_on_submit(): #if user re-searches
            info = models.Log(level="INFO", text="User searched for.")
            db.session.add(info)
            db.session.commit()
            session["search"] = search_form.search.data
            return redirect("/search")

        users = []
        users_names = []
        i = 3 #atleast 4 consecutive letters from the user input have to exist in the username
        search_string = str(session.get('search'))
        while (i < len(str(session.get('search')))): #reduces the size of the string by one each iteration until the string size equals 3.
            for p in models.User.query.filter(models.User.username.contains(search_string)): #checks if the sub string exists in any usernames in our database.
                    if p.username not in users_names: #prevents the same names from being returned multiple times.
                        users_names.append(p.username)
                        users.append(p)
            i+= 1
            search_string = search_string[:-1]
        return render_template('search.html', search=users, searchform=search_form)
    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')