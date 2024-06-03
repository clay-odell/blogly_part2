"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
def user_profile():
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
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_profile.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit User"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form["first-name"]
        user.last_name = request.form["last-name"]
        user.image_URL = request.form["img-url"]
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

## Post Views & Functionality ##

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    """Add a New Post"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return render_template('new_post.html', user=user)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show Post"""
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit Post"""
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    else:
        return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    """Delete Post"""
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(f'/users/{post.user_id}')
    else:
        return render_template('delete_post.html', post=post)
    
##Tag & Post Tag Routes    
@app.route('/tags')
def tag_list():
    """Tags View"""
    tags = Tag.query.all()
    return render_template('taglist.html', tags=tags)

@app.route('/tags/<int:tags_id>')
def show_posts_for_tag(tags_id):
    """Show Tag Detail with Posts"""
    tag = Tag.query.get_or_404(tags_id)
    return render_template('tag_detail.html', tag=tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def add_new_tag():
    """Add New Tag"""
    
    if request.method == 'POST':
        tag_name = request.form["name"]
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('add_tag.html')
    
@app.route('/tags/<int:tags_id>/edit', methods=['GET', 'POST'])
def edit_tags(tags_id):
    """Edit Tags"""
    tag = Tag.query.get_or_404(tags_id)
    if request.method == 'POST':
        tag.name = request.form["name"]
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('edit_tag.html', tag=tag)
    
@app.route('/tags/<int:tags_id>/delete', methods=['GET', 'POST'])
def delete_tag(tags_id):
    """Delete Tag"""
    tag = Tag.query.get_or_404(tags_id)
    if request.method == 'POST':
        db.session.delete(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('delete_tag.html', tag=tag)

