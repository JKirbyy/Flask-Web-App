from flask import render_template, flash
from app import db, models, app

for p in models.User.query.all():
    db.session.delete(p)
    db.session.commit()
