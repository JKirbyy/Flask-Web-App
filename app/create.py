from flask import render_template, flash, session, redirect
from app import db, models, app
from .forms import UserForm, CompleteForm, BlogForm

@app.route('/create', methods=['GET', 'POST'])
def trouble():
    if session.get('id'):
        form = BlogForm()
        if form.validate_on_submit():
            debug = models.Log(level="DEBUG", text="Story creation attempt.")
            db.session.add(debug)
            user = models.User.query.get(session.get('id'))
            story = models.Story(title=form.title.data, body=form.main.data, main_author_id=user.id, last_updater_id=user.id)
            story.users.append(user)
            story.version = 1
            db.session.add(story)
            info = models.Log(level="INFO", text="Story created.")
            db.session.add(info)
            db.session.commit()
            return redirect('/profile')
        return render_template('create.html', form=form)

    else:
        return redirect('/')
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
