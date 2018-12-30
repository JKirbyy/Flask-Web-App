from flask import render_template, flash, session, redirect, request
from app import db, models, app
from .forms import SearchForm, EmptySearchForm, BlogUpdateForm
import json

@app.route('/edit/<ID>', methods=['GET', 'POST'])
def edit(ID):
    if session.get('id'):
        new_story = models.Story.query.get(ID) #get the story to edit
        form = BlogUpdateForm(title=new_story.title, main=new_story.body) #populate the forms with the current story fields

        if form.validate_on_submit():
            debug = models.Log(level="DEBUG", text="Update form submitted.")
            db.session.add(debug)
            new_story.title = form.title.data
            new_story.body = form.main.data
            new_story.comment = form.comment.data
            new_story.last_updater_id = session.get('id')
            new_story.version +=1
            info = models.Log(level="INFO", text="Story updated.")
            db.session.add(info)
            db.session.commit()
            return redirect('/stories/' + ID) #redirects to newly updated story

        return render_template('edit.html', form=form)
    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')

@app.route('/delete/<ID>', methods=['GET', 'POST'])
def delete(ID):
    if session.get('id'):
        delete = models.Story.query.get(ID)
        db.session.delete(delete)
        info = models.Log(level="INFO", text="Story deleted.")
        db.session.add(info)
        db.session.commit()
        return redirect('/profile')

    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')

@app.route('/requests', methods=['GET', 'POST'])
def requests():
    debug = models.Log(level="DEBUG", text="Request responded to.")
    db.session.add(debug)
    db.session.commit()
    data = json.loads(request.data)
    request_id = int(data.get('request_id'))
    decision = int(data.get('decision'))
    requested = models.Requests.query.get(request_id)

    if decision == 1:  #if owner accepts author request
        requested.story.users.append(requested.user)
        info = models.Log(level="INFO", text="User authorship added.")
        db.session.add(info)
        db.session.commit()

    db.session.delete(requested) #delete the request once handled
    db.session.commit()
    return json.dumps({'status': 'OK', 'response': 'response'})


@app.route('/remove', methods=['GET', 'POST']) #called to remove users authorship rights
def remove():
    debug = models.Log(level="DEBUG", text="User remove called.")
    db.session.add(debug)
    print(session.get('id'))
    data = json.loads(request.data)
    remove_id = int(data.get('remove_id'))
    post_id = int(data.get('post_id'))
    print(remove_id)
    remove = models.User.query.get(remove_id)
    post = models.Story.query.get(post_id)
    post.users.remove(remove) #remove the user from the post
    info = models.Log(level="INFO", text="User removed.")
    db.session.add(info)
    db.session.commit()
    return json.dumps({'status': 'OK', 'response': 'response'})

@app.route('/stories/<ID>', methods=['GET', 'POST'])
def post(ID):
    if session.get('id'):
        info = models.Log(level="INFO", text="Story viewed.")
        db.session.add(info)
        db.session.commit()
        main = False
        author = False
        requesters = []
        capped_users = []
        requested = False
        author_count = 0
        post=models.Story.query.get(ID)
        last_author = models.User.query.get(post.last_updater_id)
        main_author = models.User.query.get(post.main_author_id)

        for r in post.requests:
            requesters.append(r)
            if r.user.id == session.get('id'):
                requested = True #user has requested to author the story

        if post.main_author_id == session.get('id'):
            main = True #user is main author of story

        for u in post.users:
            author_count += 1
            if author_count < 5:
                capped_users.append(u) #only displays 4 authors on by line to prevent display overflow issues
            if session.get('id') == u.id:
                author = True #user is author of story
        return render_template('post.html', requested=requested, user_id = session.get('id'), last_author=last_author, post=post, capped=capped_users, main=main, author=author, author_count=author_count, main_author=main_author, requesters=requesters, req_count=len(requesters))

    else:
        warn = models.Log(level="WARN", text="Un-authorised user attempting to access page.")
        db.session.add(warn)
        db.session.commit()
        return redirect('/')