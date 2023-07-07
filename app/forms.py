from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    DateField,
    SelectField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    # perform validation only when entered username and email are different
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class RegisterAsDonorForm(FlaskForm):
    states = [
        ("", "Select State"),
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Arunachal Pradesh", "Arunachal Pradesh"),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jharkhand", "Jharkhand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telangana", "Telangana"),
        ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("Uttarakhand", "Uttarakhand"),
        ("West Bengal", "West Bengal"),
        ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
        ("Chandigarh", "Chandigarh"),
        (
            "Dadra and Nagar Haveli and Daman and Diu",
            "Dadra and Nagar Haveli and Daman and Diu",
        ),
        ("Delhi", "Delhi"),
        ("Ladakh", "Ladakh"),
        ("Lakshadweep", "Lakshadweep"),
        ("Puducherry", "Puducherry"),
    ]

    DonorName = StringField("Donor Full Name", validators=[DataRequired()])
    DateOfBirth = DateField(
        "Date of Birth", validators=[DataRequired()], format="%Y-%m-%d"
    )
    BloodType = SelectField(
        "Blood Type",
        choices=[
            ("", "Select Blood Type"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-"),
        ],
    )
    LastDonateDate = DateField(
        "Last Donate Date", validators=[DataRequired()], format="%Y-%m-%d"
    )
    PhoneNumber = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=15),
            Regexp(
                r"^\+?[0-9]+$",
                message="Invalid phone number format. Only digits and '+' are allowed.",
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    StreetAddress = StringField("Street Address", validators=[DataRequired()])
    City = StringField("City ", validators=[DataRequired()])
    State = SelectField("State / Province", choices=states, validators=[DataRequired()])
    country_code = StringField("PinCode", validators=[DataRequired()])
    Country = SelectField("Country", choices=[('India', 'India')], validators=[DataRequired()])
    AgreeToTerms = BooleanField(
        "I agree to the terms and conditions",
        validators=[
            DataRequired(message="You must agree to the terms and conditions.")
        ],
        description="By checking this box, I acknowledge that my information will be recorded and may be shared with individuals in need of blood. In case of an emergency, either we or they may contact me for assistance.",
    )
    Submit = SubmitField("Register")
