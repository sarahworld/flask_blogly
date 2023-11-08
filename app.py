"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def index():
    users = User.query.all();
    print(users)
    return render_template("user_list.html", page_title='user_list', user_list=users)

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", page_title='User Detail Page', user = user )

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

    users = User.query.all();
    return render_template("user_list.html", page_title='user_list', user_list=users)

@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", page_title='Edit User Form', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    edit_user = User.query.get_or_404(user_id)

    edit_user.first_name=first_name, 
    edit_user.last_name=last_name, 
    edit_user.image_url=image_url

    db.session.add(edit_user);
    db.session.commit();

    users = User.query.all();
    return render_template("user_list.html", page_title='user_list', user_list=users)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    users = User.query.all();
    return render_template("user_list.html", page_title='user_list', user_list=users)


