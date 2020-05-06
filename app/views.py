from app import app, db ,login_manager
import os
import datetime

from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required

from app.forms import RegisterForm, LoginForm, UploadForm
from app.models import Users,Posts

from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
#place routes and functions below

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
#Accepts user information and saves it to the database
@app.route('/api/users/register', methods=['POST','GET'])
def userform():
    date=datetime.datetime.now()
    joined_on= date.strftime('%B,%d,%Y')
    form=RegisterForm()
    if request.method=='POST'and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        firstname=form.firstname.data
        lastname=form.lastname.data
        email= form.email.data
        location= form.location.data
        biography= form.biography.data
        photo= form.photo.data
        filename=secure_filename(photo.filename)

        photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        user=Users(username=username,password=password,firstname=firstname,lastname=lastname,
                email=email,location=location,biography=biography,profile_photo=filename,joined_on=joined_on)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully Registered")
        return redirect(url_for('userform'))
    #flash("Registeration unsuccessful")
    return render_template("userform.html",form=form)

#Accepts login credentials as username and password

@app.route('/api/auth/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
            return redirect(url_for("home"))
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user= Users.query.filter_by(username=username).first()

        if user is not None and  check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successful",'success')
            return redirect(url_for('home'))
        else:
            flash('Username or password is incorrect', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html",form=form)



#logout a user
@app.route('/api/auth/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('you have been logout','danger')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))



@app.route('/api/users/<int:user_id>/posts',methods=['GET','POST'])
#@login_required
def Post(user_id):
    #post=Posts.query.filter_by(user_id=user_id).first()
    #return render_template("uploadpost.html",post=post)
    date=datetime.datetime.now()
    created_on= date.strftime('%B,%d,%Y')
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        photo= form.photo.data
        caption= form.caption.data
        post=Posts(user_id=user_id,photo=photo,caption=caption,created_on=created_on)
        db.session.add(post)
        db.session.commmit()
        flash("Successfully updated")
        return redirect(url_for('profile'))

    return render_template('uploadpost.html',form=form)



















    if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0", port="8080")