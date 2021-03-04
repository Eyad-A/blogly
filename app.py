from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag 

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
    tags = Tag.query.all()
    return render_template("/add_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """ handle the form submission for adding a new post """

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user=user,
        tags=tags 
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
    tags = Tag.query.all()
    return render_template('post_edit.html', post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_edit_post(post_id):
    """ handle form submission for post edits """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


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


#################
## Tags Routes ##
#################

@app.route('/tags')
def show_tags():
    """Show all tags"""

    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_show(tag_id):
    """ Show details on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)


@app.route('/tags/new')
def new_tag_form():
    """ show the create a new tag form"""

    posts = Post.query.all()
    return render_template('add_tag.html')


@app.route('/tags/new', methods=['POST'])
def process_new_tag():
    """Handle form submission for new tags"""

    new_tag = Tag(name=request.form['tag_name'])

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def edit_tags_form(tag_id):
    """Show a form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def process_edit_tag(tag_id):
    """Handle form submission for editing tags"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_delete(tag_id):
    """Handle form submission for deleting tags"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

