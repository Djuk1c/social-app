from operator import pos
from flask import Flask, render_template, Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from .models import Posts, User
from sqlalchemy import func
from . import db
import time
import ast

main = Blueprint('main', __name__)
#
@main.route("/")
def index():
    posts = Posts.query.order_by(Posts.postTime.desc()).all()
    return render_template('index.html', posts=posts)

#
@main.route("/login")
def login():
    return render_template('login.html')
@main.route("/login", methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(func.lower(User.username)==func.lower(username)).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login'))

    login_user(user)
    return redirect(url_for('main.index'))

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#
@main.route('/register')
def register():
    return render_template('register.html')
@main.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(func.lower(User.username)==func.lower(username)).first()

    if user:
        flash('Username is already taken.')
        return redirect(url_for('main.register'))
    elif len(username) < 5 or len(password) < 5:
        flash('Username and/or password must be longer than 5 characters.')
        return redirect(url_for('main.register'))
    
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    flash('You registered sucessfully. Please log in.')
    return redirect(url_for('main.login'))

#
@main.route('/submit_post')
def submit():
    return redirect(url_for('main.index'))
@main.route('/submit_post', methods=['POST'])
@login_required
def submit_post():
    content = request.form['status']
    posterName = current_user.username
    likes = []
    #postTime = int(time.time())

    if len(content) < 2:
        flash('Your post must be at least 2 characters long.')
        return redirect(url_for('main.index'))
    
    new_post = Posts(posterName=posterName, content=content, likes=repr(likes))
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('main.index'))

#
@main.route('/edit_post')
def edit():
    return redirect(url_for('main.index'))
@main.route('/edit_post', methods=['POST'])
@login_required
def edit_post():
    content = request.form['edit_post']
    postId = request.args.get('post')
    
    if len(content) < 2:
        flash('Your post must be at least 2 characters long.')
        return redirect(url_for('main.index'))
    
    postToUpdate = Posts.query.get_or_404(postId)
    if postToUpdate.posterName == current_user.username:
        postToUpdate.content = content
        db.session.commit()

    return redirect(url_for('main.index'))


#
@main.route('/delete_post')
@login_required
def delete_post():
    postId = request.args.get('post')

    postToDelete = Posts.query.get_or_404(postId)
    if postToDelete.posterName == current_user.username:
        db.session.delete(postToDelete)
        db.session.commit()

    return redirect(url_for('main.index'))


#
@main.route('/like_post')
@login_required
def like_post():
    postId = request.args.get('post')

    postToLike = Posts.query.get_or_404(postId)
    oldPostArray = ast.literal_eval(postToLike.likes)
    if current_user.username not in oldPostArray:
        oldPostArray.append(current_user.username)
        postToLike.likes = repr(oldPostArray)
        db.session.commit()
    else:
        oldPostArray.remove(current_user.username)
        postToLike.likes = repr(oldPostArray)
        db.session.commit()
    
    return redirect(url_for('main.index'))