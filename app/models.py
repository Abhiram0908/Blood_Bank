from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Date


# Extension to manage sessions
@login_manager.user_loader
def load_user(email_id):
    return User.query.get(int(email_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    donors = db.relationship('Donor', backref='Email', lazy=True)

    # How object is printed
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DonorName = db.Column(db.Text, nullable=False)
    DateOfBirth = db.Column(Date, nullable=False)
    BloodType = db.Column(db.String(), nullable=False)
    LastDonateDate = db.Column(Date, nullable=False)
    PhoneNumber = db.Column(db.String(), nullable=False)
    StreetAddress = db.Column(db.Text, nullable=False)
    City = db.Column(db.String(), nullable=False)
    State = db.Column(db.String(), nullable=False)
    pin_code = db.Column(db.String(), nullable=False)
    Country = db.Column(db.String(), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# How object is printed
    def __repr__(self):
        return f"Donor('{self.DonorName}', '{self.BloodType}', '{self.PhoneNumber}')"