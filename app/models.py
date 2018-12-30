from app import db

stor = db.Table('stor',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('story_id', db.Integer, db.ForeignKey('story.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    password = db.Column(db.String(15))
    stories = db.relationship('Story', secondary = stor, backref=db.backref('users', lazy='dynamic')) #stories they author
    requests = db.relationship('Requests', backref='user', lazy='dynamic') #requests for authorship

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10))
    text = db.Column(db.String(300))

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    story_id  = db.Column(db.Integer, db.ForeignKey('story.id'))


class Story (db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(50000))
    main_author_id =  db.Column(db.Integer) #stores the id of the author who owns the story
    requests = db.relationship('Requests', backref='story', lazy='dynamic')
    comment = db.Column(db.String(500)) #added on story update
    last_updater_id = db.Column(db.Integer) #added on story update
    version = db.Column(db.Integer)

