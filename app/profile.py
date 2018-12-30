from flask import render_template, flash, session, redirect
from app import db, models, app
from .forms import UserForm, CompleteForm, SearchForm, PasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('id'):
        user_form = PasswordForm()
        search_form = SearchForm()
        follow_list=[] #redundant
        follower_list=[] #redundant
        stories = []
        if user_form.validate_on_submit(): #called when user opts to change password
            u = models.User.query.get(session.get('id'))
            u.password = generate_password_hash(user_form.password.data, method='pbkdf2:sha256', salt_length=6)
            db.session.commit()

        if search_form.validate_on_submit():
            session["search"] = search_form.search.data
            return redirect("/search")

        user = models.User.query.get(session.get('id'))
        for s in user.stories:
            if s.main_author_id == session.get('id'):
                stories.append(s) #prepare users owned stories for display

        return render_template('profile.html', form=user_form, searchform=search_form, blog=stories, count=len(stories),  main_author= user.username, follows=follow_list, follows_amount=len(follow_list), follower_amount=len(follower_list))
    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')