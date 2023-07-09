import secrets, os
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RegisterAsDonorForm,
)
from app.models import User, Donor
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Your account has been created!, You are now able to login ", "success"
        )  # Flash message
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Please check your Email or Password!", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You Loged out", "success")
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    form_picture.save(picture_path)

    return picture_fn


# put restrictions over some pages (must login)
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been Updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/donor/registration", methods=["GET", "POST"])
@login_required
def donor_register():
    form = RegisterAsDonorForm()
    if form.validate_on_submit():
        donor = Donor(
            DonorName=form.DonorName.data,
            BloodType=form.BloodType.data,
            DateOfBirth=form.DateOfBirth.data,
            LastDonateDate=form.LastDonateDate.data,
            PhoneNumber=form.PhoneNumber.data,
            Email=current_user,
            StreetAddress=form.StreetAddress.data,
            City=form.City.data,
            State=form.State.data,
            pin_code=form.pin_code.data,
            Country=form.Country.data,
        )
        db.session.add(donor)
        db.session.commit()
        flash("You are now registered as a donor", "success")
        return redirect(url_for("donor_data"))

    return render_template("donor_register.html", title="RegisterDonar", form=form)


@app.route("/donor/registration/Donor_data")
@login_required
def donor_data():
    donor = Donor.query.all()
    return render_template("donor_data.html", title="Donor_Data", donor=donor)
