from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm,RegistrationForm,EditProfileForm,ItemForm,EditTodoForm
from flask_login import current_user, login_user,logout_user,login_required
import sqlalchemy as sa
from app import db
from app.models import User,Todo
from flask import request
from urllib.parse import urlsplit



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Miguel'}
    todos = [
        {
            'author': {'username': 'John'},
            'title': 'finish project 1',
            'content':'complete last review of project',
            'complete':'doing'
        },
        {
            'author': {'username': 'Mike'},
            'title': 'finish project 5',
            'content':'complete requirement analysis of project',
            'complete':'todo'
        }
    ]
    todos = db.session.query(Todo).all()
    return render_template('index.html',todos=todos)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        # flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           form=form)



@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form=ItemForm()
    if form.validate_on_submit():
        item = Todo(
            title=form.title.data,
            content=form.content.data,
            complete=form.complete.data,
            user_id = current_user.id
        )
        db.session.add(item)
        db.session.commit()
        # flash('Your item is now live!')
        return redirect(url_for('index'))

    return render_template('add.html', form=form)



@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user=current_user 
    form = EditTodoForm()
    todo = Todo.query.filter_by(id =id,user_id = current_user.id).first()

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.content= form.content.data
        todo.complete = form.complete.data
        db.session.commit()
        return redirect(url_for('index'))
        
    elif request.method == 'GET':
        form.title.data = todo.title
        form.content.data = todo.content
        form.complete.data = todo.complete
    return render_template('edit.html',form=form)

@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
    todo = Todo.query.filter_by(id =id,user_id = current_user.id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))