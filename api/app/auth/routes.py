
from flask import (render_template, redirect, url_for,
                   request, current_app, session, flash)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash

from app import login_manager, db
from . import auth_bp
from .forms import SignupForm, LoginForm, ProfileForm, PasswordForm
from .models import User, Profile

import requests
import json


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('public.index_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):

            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index_page')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/profile')
@login_required
def profile():
    profile = Profile.get_my_profile(current_user.get_id())
    user = User.get_by_id(current_user.get_id())
    return render_template('auth/profile.html', profile=profile, user=user)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@auth_bp.route('/password_change', methods=["GET", "POST"])
@login_required
def user_password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('auth.profile'))

    return render_template('auth/password_change.html', form=form)
