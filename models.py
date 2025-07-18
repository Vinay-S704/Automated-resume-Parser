from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    skills = db.relationship('Skill', backref='candidate', lazy=True)
    education = db.relationship('Education', backref='candidate', lazy=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(128))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
