from flask import render_template, url_for, flash, redirect, request, send_file
from app import app, db, bcrypt
from PIL import Image
import os
import secrets
from app.forms import RegistrationForm, LoginForm, JobForm, ApplicationForm
from app.models import User, Jobs, Application
from flask_login import login_user, current_user, logout_user, login_required
import random

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.usertype == 'Alumno':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Compañía':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, usertype=form.usertype.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('¡Tu cuenta a sido creada con exito!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.usertype == 'Alumno':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Compañía':
            return redirect(url_for('posted_jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print('password clear')
            if form.usertype.data == user.usertype and form.usertype.data == 'Alumno':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
            elif form.usertype.data == user.usertype and form.usertype.data == 'Compañía':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
            else:
                flash('Iniciar sesión sin éxito. Por favor verifique el correo electrónico, la contraseña y el tipo de usuario.', 'danger')
        else:
            flash('Iniciar sesión sin éxito. Por favor verifique el correo electrónico, la contraseña y el tipo de usuario.', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))

def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
@login_required
def post_cvs(jobid):
    form = ApplicationForm()
    job = Jobs.query.filter_by(id=jobid).first()
    if form.validate_on_submit():
        if not form.cv.data:
            flash('Porfavor sube un CV en pdf', 'danger')
            return render_template('post_cvs.html', form=form)
        
        cv_filename = form.cv.data.filename
        application = Application(
            gender=form.gender.data,
            degree=form.degree.data,
            industry=form.industry.data,
            experience=form.experience.data,
            cover_letter=form.cover_letter.data,
            application_submiter=current_user,
            application_jober=job,
            cv=cv_filename
        )

        picture_file = save_picture(form.cv.data)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('show_jobs'))
    return render_template('post_cvs.html', form=form)

@app.route("/post_jobs", methods=['GET', 'POST'])
@login_required
def post_jobs():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data,
                   company=current_user.username,
                   industry=form.industry.data,
                   description=form.description.data,
                   link=form.link.data,
                   job_applier=current_user)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('posted_jobs'))
    return render_template('post_jobs.html', form=form)

@app.route("/posted_jobs")
@login_required
def posted_jobs():
    jobs = Jobs.query.all()
    
    # Get the selected industry from the request
    selected_industry = request.args.get('industry')
    # Filter jobs by industry if an industry is selected
    if selected_industry:
        selected_industry = selected_industry.replace('+', ' ')
        jobs = Jobs.query.filter_by(industry=selected_industry).all()
    return render_template('show_jobs.html', jobs=jobs)


@app.route("/show_applications/<jobid>", methods=['GET'])
@login_required
def show_applications(jobid):
    applications = Application.query.filter_by(job_id=jobid).order_by(Application.degree, Application.experience.desc()).all()
    return render_template('show_applications.html', applications=applications)

@app.route("/meeting/<application_id>")
@login_required
def meeting(application_id):
    applicant_id = Application.query.get(int(application_id)).user_id
    applicant = User.query.get(applicant_id)
    return render_template('meeting.html', applicant=applicant)

@app.route("/", methods=['GET', 'POST'])
@app.route("/show_jobs", methods=['GET', 'POST'])
def show_jobs():
    # Get all jobs
    jobs = Jobs.query.all()
    
    # Get the selected industry from the request
    selected_industry = request.args.get('industry')
    # Filter jobs by industry if an industry is selected
    if selected_industry:
        selected_industry = selected_industry.replace('+', ' ')
        jobs = Jobs.query.filter_by(industry=selected_industry).all()

    return render_template('show_jobs.html', jobs=jobs)

@app.route("/resume/<id>", methods=['GET'])
def resume(id):
    cv = Application.query.get(int(id)).cv
    return render_template('resume.html', cv=cv)

