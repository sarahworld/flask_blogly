"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()

@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    for post in posts:
        friendly_date = post.created_at.strftime("%a %b %-d  %Y, %-I:%M %p");
    return render_template("Homepage.html", posts=posts, page_title='Homepage', friendly_date=friendly_date)

@app.route('/users')
def index():
    users = User.query.all();
    return render_template("user_list.html", page_title='user_list', user_list=users)

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", page_title='User Detail Page', user = user, posts=user.posts)

@app.route("/users/new")
def show_add_user_form():
    return render_template("add_user_form.html", page_title='New User Form')

@app.route("/users/new", methods=["POST"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url);
    db.session.add(new_user);
    db.session.commit();

    return redirect(f"/users")

    
@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", page_title='Edit User Form', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    edit_user = User.query.get_or_404(user_id)

    edit_user.first_name = request.form["first_name"]
    edit_user.last_name = request.form["last_name"]
    edit_user.image_url = request.form["image_url"]

    db.session.add(edit_user);
    db.session.commit();

    users = User.query.all();
    return redirect(f"/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(f"/users")


@app.route("/posts/<int:post_id>")
def post_detail_page(post_id):
    post = Post.query.get_or_404(post_id);
    posted_by = post.user.get_full_name();
    
    return render_template("post_details.html", post=post, posted_by=posted_by);


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_new_post_form(user_id):
    user=User.query.get_or_404(user_id);
    return render_template("add_new_post.html", user=user, page_title='New Post Form')


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    user=User.query.get_or_404(user_id);

    title = request.form['title'];
    content = request.form['content'];

    new_post = Post(title=title, content=content, user_id=user_id);
    db.session.add(new_post);
    db.session.commit();

    return redirect(f"/users/{new_post.user_id}")
  

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_page(post_id):
    edit_post = Post.query.get_or_404(post_id);
    return render_template('edit_post_form.html', post=edit_post, user=edit_post.user, page_title="Post Edit Page")

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id);
    post.title = request.form['title'];
    post.content = request.form['content'];

    db.session.add(post);
    db.session.commit();
    
    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id);
    user_id = post.user_id;
    Post.query.filter_by(id=post_id).delete();
    db.session.commit()

    return redirect(f"/users/{user_id}")