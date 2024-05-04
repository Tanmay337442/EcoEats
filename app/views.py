from flask import render_template, flash, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, date
from forms import UserForm, LoginForm, UserUpdateForm, FoodForm
from models import Users, Foods, db

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        user_username = Users.query.filter_by(
            username=form.username.data).first()
        if user is None and user_username is None:
            hashed_pass = generate_password_hash(
                form.password_hash.data, "pbkdf2:sha256")
            user = Users(username=form.username.data,
                         email=form.email.data, password_hash=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash("User created", "alert alert-success alert-dismissible fade show")
            form.username.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            return redirect(url_for('views.login'))
        elif user and user_username:
            flash("Username and email are taken",
                  "alert alert-danger alert-dismissible fade show")
            form.username.data = ''
            form.email.data = ''
        elif user and not user_username:
            flash("Email is taken",
                  "alert alert-danger alert-dismissible fade show")
            form.email.data = ''
        elif user_username and not user:
            flash("Username is taken",
                  "alert alert-danger alert-dismissible fade show")
            form.username.data = ''
    all_users = Users.query.order_by(Users.date_added)
    return render_template('register.html', form=form, all_users=all_users)

# DO ALL OF LOGIN
@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("You are logged in",
                      "alert alert-success alert-dismissible fade show")
                return redirect(url_for('views.profile'))
            else:
                flash("Wrong password - try again",
                      "alert alert-danger alert-dismissible fade show")
        elif user is None:
            user = Users.query.filter_by(email=form.username.data).first()
            if user:
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("You are logged in",
                          "alert alert-success alert-dismissible fade show")
                    return redirect(url_for('views.profile'))
                else:
                    flash("Wrong password - try again",
                          "alert alert-danger alert-dismissible fade show")
        else:
            flash("User does not exist",
                  "alert alert-danger alert-dismissible fade show")
    return render_template('login.html', form=form)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserUpdateForm()
    if form.validate_on_submit():
        if Users.query.filter_by(username=form.username.data).first() and form.username.data != current_user.username:
            flash('Username is taken',
                  "alert alert-danger alert-dismissible fade show")
            current_user.email = form.email.data
        elif Users.query.filter_by(email=form.email.data).first() and form.email.data != current_user.email:
            flash('Email address is taken',
                  "alert alert-danger alert-dismissible fade show")
            current_user.username = form.username.data
        else:
            current_user.email = form.email.data
            current_user.username = form.username.data
            db.session.commit()
            flash("User updated",
                  "alert alert-success alert-dismissible fade show")
    return render_template('user_settings.html', form=form)


@views.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    if current_user.id == user_to_delete.id:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted",
                  "alert alert-success alert-dismissible fade show")
        except:
            flash("Something went wrong... try again later",
                  "alert alert-danger alert-dismissible fade show")
    return redirect(url_for('views.register'))

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@views.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out",
          "alert alert-success alert-dismissible fade show")
    return redirect(url_for('views.login'))

@views.route('/add-food', methods=['GET', 'POST'])
@login_required
def add_food():
    form = FoodForm()
    if form.validate_on_submit():
        user = current_user.id
        food = Foods(user_id=user, name=form.name.data, expiry_date=form.date.data)
        db.session.add(food)
        db.session.commit()
        flash(f"{food.name} added",
              "alert alert-success alert-dismissible fade show")
        form.name.data = ''
        form.date.data = ''
        return redirect(url_for('views.foods'))
    return render_template('add_food.html', form=form)

@views.route('/foods/<int:id>')
@login_required
def food(id):
    food = Foods.query.get_or_404(id)
    if current_user.id == food.user.id:
        return render_template('food.html', food=food)
    else:
        flash("Food does not exist",
              "alert alert-danger alert-dismissible fade show")
        return redirect(url_for('views.foods'))


@views.route('/food/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def food_settings(id):
    food = Foods.query.get_or_404(id)
    if current_user.id == food.user.id:
        form = FoodForm()
        if form.validate_on_submit():
            food.name = form.name.data
            food.expiry_date = form.date.data
            db.session.commit()
            flash("Food updated",
                  "alert alert-success alert-dismissible fade show")
            return redirect(url_for('views.foods'))
        form.name.data = food.name
        form.date.data = food.expiry_date
        return render_template('food_settings.html', form=form)
    else:
        flash("Food does not exist",
              "alert alert-danger alert-dismissible fade show")
        return redirect(url_for('views.foods'))


@views.route('/foods/delete/<int:id>')
@login_required
def delete_food(id):
    food_to_delete = Foods.query.get_or_404(id)
    if current_user.id == food_to_delete.user.id:
        try:
            db.session.delete(food_to_delete)
            db.session.commit()
            flash("Food deleted",
                  "alert alert-success alert-dismissible fade show")
            return redirect(url_for('views.foods'))
        except:
            flash("Something went wrong... try again later",
                  "alert alert-danger alert-dismissible fade show")
            return redirect(url_for('views.foods'))
    else:
        flash("This course does not exist",
              "alert alert-danger alert-dismissible fade show")
        return redirect(url_for('views.foods'))


@views.route('/foods')
@login_required
def foods():
    foods = Foods.query.order_by(Foods.expiry_date)
    createdfoods = []
    for food in foods:
        if current_user.id == food.user.id:
            createdfoods.append(food)
    return render_template('foods.html', foods=createdfoods)


@views.route('/mail')
@login_required
def mail():
    foods = Foods.query.order_by(Foods.expiry_date)
    mails = []
    expiry_dates = []
    current = date.today()
    for food in foods:
        expiry = food.expiry_date.date()
        delta = expiry - current
        if current_user.id == food.user.id and delta.days >= 1 and delta.days <= 3:
            print(delta)
            mails.append(food)
    return render_template('mail.html', mails=mails, date_current=current)