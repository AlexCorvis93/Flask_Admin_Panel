from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(500), nullable=True)
    profiles = db.relationship('Profile', backref='users')

    def __repr__(self):
        return f"{self.login}"


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id')) #должность с правами доступа к определенным действиям в админке

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.name}:{self.last_name}"


class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    profiles = db.relationship('Profile', backref='position')

    def __repr__(self):
        return f"{self.name}"