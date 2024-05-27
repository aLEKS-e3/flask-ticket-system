from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"User: {self.username}"


@login.user_loader
def load_user(id: int) -> User:
    return User.query.get(id)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="group", lazy="dynamic")
    tickets = db.relationship("Ticket", backref="group", lazy="dynamic")

    def __repr__(self) -> str:
        return f"Group: {self.name}"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default="Pending")
    note = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    def __repr__(self) -> str:
        return f"Ticket: {self.id}"
