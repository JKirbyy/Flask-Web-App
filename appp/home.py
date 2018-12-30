from flask import render_template, flash, session, redirect
from app import db, models, app
from .forms import SearchForm

@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('id'):
        search_form = SearchForm()
        user = models.User.query.get(session.get('id'))
        username = user.username
        if search_form.validate_on_submit():
            session["search"] = search_form.search.data
            return redirect("/search")

        return render_template('blog.html', searchform=search_form, blog=user.stories, username=username)
    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect("/")

