"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/blogly_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def show_user_list():
    """Show List of Users"""
    users = User.query.all()
    return render_template('/userlist.html', users=users)

@app.route('/users')
def user_list_with_add_button():
    """User Profile View With Add Button"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_new_user():
    """Add a New User"""
    if request.method == 'POST':
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        user_img_url = request.form.get("img-url")
        if not user_img_url:
            user_img_url = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg'
        
        user = User(first_name=first_name, last_name=last_name, image_URL=user_img_url)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_profile_view(user_id):
    """User Profile View"""
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit User"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_URL = request.form['img-url']
        if not user.image_URL:
            user.image_URL = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg'

        db.session.commit()
        return redirect('/users')
    else:
        return render_template('edit_user.html', user=user)
    
@app.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    """Delete User from Database"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('delete_user.html', user=user)



