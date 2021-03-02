from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def show_index():
    """ redirect to /users for now """

    return redirect('/users')


@app.route("/users")
def user_listing():
    """ show all users """

    users = User.query.all()
    return render_template('user_listing.html', users=users)


@app.route("/users/new", methods=["GET"])
def new_user():
    """ show the create user form """

    return render_template("create_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """ handle form submission for adding new users """

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """ show user details """

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    """ show user edit form """

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    """ handle user edits """

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ delete a user """
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


### Posts routes ###

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """ show the add a new post form for that user """

    user = User.query.get_or_404(user_id)
    return render_template("/add_post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """ handle the form submission for adding a new post """

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user=user
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ show a post """

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """ show edit post form """

    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_edit_post(post_id):
    """ handle form submission for post edits """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ delete a post """
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")