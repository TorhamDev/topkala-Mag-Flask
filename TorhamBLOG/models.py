from TorhamBLOG import db
import datetime
class articles(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.Text , nullable=False , unique=True)
    name = db.Column(db.String(80) , nullable=False)
    title = db.Column(db.String(300) , nullable=False , unique=True)
    photo_title_name = db.Column(db.Text , nullable=False , unique=True)
    article_tag = db.Column(db.String(50) , nullable=False)
    publish_time = db.Column(db.Text , nullable=False)

class USER(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(80) , nullable=False , unique=True)
    email = db.Column(db.Text , nullable=False , unique=True)
    user_name = db.Column(db.Text , nullable=False , unique=True)
    password = db.Column(db.Text , nullable=False , unique=True)


db.create_all()