from app import db

match = db.Table('match',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime)
    number = db.Column(db.String(15)) #larger than expected maximum value for unexpected inputs eg. a foreign country
    email = db.Column(db.String(50)) #larger than expected maximum value to be on the safe side
    games = db.relationship('Game', secondary=match, lazy='dynamic', backref=db.backref('participants', lazy='dynamic')) #check

class Game (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    winner_score = db.Column(db.Integer)
    loser_score = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    draw = db.Column(db.Boolean)
