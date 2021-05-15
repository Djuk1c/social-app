from operator import pos
from flask import Flask, render_template, Blueprint, redirect, url_for, request, flash
from flask.signals import request_tearing_down
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from .models import Posts, User, Comments
from sqlalchemy import func
from . import db
from PIL import Image
import os, ast, uuid

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

@main.route("/")
def index():
    posts = Posts.query.order_by(Posts.postTime.desc()).all()
    return render_template('index.html', posts=posts)


@main.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
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


@main.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
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
        user = User.query.filter(func.lower(User.username)==func.lower(username)).first()
        login_user(user)

        flash('You registered sucessfully.')
        return redirect(url_for('main.index'))


@main.route('/submit_post', methods=['POST', 'GET'])
@login_required
def submit():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    
    elif request.method == 'POST':
        content = request.form['status']
        posterName = current_user.username
        likes = []

        if len(content) < 2:
            flash('Your post must be at least 2 characters long.')
            return redirect(request.referrer)

        genName = 'none'
        if request.files.get('picUpload', None):
            picture = request.files['picUpload']
            if os.path.splitext(picture.filename)[1] not in ALLOWED_EXTENSIONS:
                flash('Not allowed file extension.')
                return redirect(request.referrer)

            genName = str(uuid.uuid4())
            path = os.path.join('static/uploads', genName + os.path.splitext(picture.filename)[1])
            picture.save(path)
            # Converting the image to PNG and removing the old one.
            if os.path.splitext(picture.filename)[1] != '.png':
                imToConvert = Image.open(path)
                imToConvert.save(os.path.join('static/uploads', genName + '.png'))
                os.remove('static/uploads/' + genName + os.path.splitext(picture.filename)[1])
        
        new_post = Posts(posterName=posterName, content=content, likes=repr(likes), image=genName + '.png')
        db.session.add(new_post)
        db.session.commit()

        return redirect(request.referrer)


@main.route('/comment_post', methods=['POST', 'GET'])
@login_required
def comment():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    elif request.method == 'POST':
        content = request.form['comment_post']
        postId = request.args.get('post')
        posterName = current_user.username
        
        if len(content) < 2:
            flash('Your post must be at least 2 characters long.')
            return redirect(request.referrer)

        orgPost = Posts.query.filter_by(id=postId).first()
        if orgPost:
            new_comment = Comments(posterName=posterName, content=content, post_id=postId)
            db.session.add(new_comment)
            db.session.commit()

    return redirect(request.referrer)

@main.route('/edit_post', methods=['POST', 'GET'])
@login_required
def edit():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    
    elif request.method == 'POST':
        content = request.form['edit_post']
        postId = request.args.get('post')
        
        if len(content) < 2:
            flash('Your post must be at least 2 characters long.')
            return redirect(request.referrer)
        
        postToUpdate = Posts.query.get_or_404(postId)
        if postToUpdate.posterName == current_user.username:
            postToUpdate.content = content
            db.session.commit()

        return redirect(request.referrer)


@main.route('/delete_post')
@login_required
def delete_post():
    postId = request.args.get('post')

    postToDelete = Posts.query.get_or_404(postId)
    if postToDelete.posterName == current_user.username:
        db.session.delete(postToDelete)
        db.session.commit()
        if postToDelete.image != 'none.png':
            os.remove('static/uploads/' + postToDelete.image)

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
    
    return redirect(request.referrer)

@main.route('/post')
def post():
    postId = request.args.get('id')

    post = Posts.query.filter_by(id=postId).first()

    comments = db.session.query(Comments).filter(Comments.post_id == postId).all()
    comments = comments[::-1]

    return render_template('post.html', post=post, comments=comments)

