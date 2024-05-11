# routes.py
from flask import Blueprint, render_template, redirect, url_for, jsonify, request, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from controllers.user import add_user_function, edit_user_function, delete_user_function
from models.user import User, Task, Employee, Job, Supervisor
import sys
from models import user

from flask_login import current_user
from werkzeug.security import generate_password_hash


main = Blueprint('main', __name__) #routename = main

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        name = request.form['name']  # Define the variable "name" by retrieving it from the form data

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)

        user.db.session.add(new_user)
        user.db.session.commit()

        
        flash('User has been created!')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(name=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('main.login'))
        if user.role == 'Admin' or user.role == 'Supervisor':
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('You are not an admin.')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))


@main.route('/CRUD', methods=['GET'])
@login_required
def home():
    data = User.get_all()
    return render_template('CRUD.html', data=data, role=current_user.role)

@main.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if the user already exists in the database
        if User.query.filter_by(email=email).first():
            flash('A user with that email already exists.')
            return redirect(url_for('main.add_user'))

        # Hash the password and create a new user instance
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)

        # Add the new user to the database
        user.db.session.add(new_user)
        user.db.session.commit()
        flash('New user added successfully!')

        if role == 'Employee':
            employee = Employee(user_id=new_user.id)
            user.db.session.add(employee)
            user.db.session.commit()
            flash('Employee added successfully!')
        elif role == 'Supervisor':
            supervisor = Supervisor(user_id=new_user.id)
            user.db.session.add(supervisor)
            user.db.session.commit()
            flash('Supervisor added successfully!')
        else:
            pass

    # If it's a GET request, just display the Add User form
    return render_template('adduser.html', role=current_user.role)


@main.route('/edituser/<int:id>', methods=['GET','POST'])
@login_required
def edit_user(id):
    user = User.get_by_id(id)
    print(user.id)
    data = edit_user_function(user)
    return render_template('edituser.html', user=user, data=data, role=current_user.role)

@main.route('/deleteuser/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.get_by_id(id)
    print (user, file=sys.stderr)
    delete_user_function(user)
    return redirect(url_for('main.home', role=current_user.role))

# Additional routes for Tasks, Employees, Jobs, and Supervisors
@main.route('/supervisors', methods=['GET', 'POST'])
def supervisors():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        job_id = request.form.get('job_id')
        supervisor = Supervisor(user_id=user_id, job_id=job_id)
        user.db.session.add(supervisor)
        user.db.session.commit()
        flash('Supervisor added successfully!')
    supervisors = Supervisor.query.all()
    return render_template('supervisors.html', supervisors=supervisors, role=current_user.role)

@main.route('/supervisors/edit/<int:id>', methods=['GET', 'POST'])
def edit_supervisor(id):
    supervisor = Supervisor.query.get_or_404(id)
    if request.method == 'POST':
        supervisor.user_id = request.form.get('user_id')
        supervisor.job_id = request.form.get('job_id')
        user.db.session.commit()
        flash('Supervisor updated successfully!')
        return redirect(url_for('main.supervisors'))
    return render_template('edit_supervisor.html', supervisor=supervisor, role=current_user.role)

@main.route('/supervisors/delete/<int:id>', methods=['POST'])
def delete_supervisor(id):
    supervisor = Supervisor.query.get_or_404(id)
    user.db.session.delete(supervisor)
    user.db.session.commit()
    flash('Supervisor deleted successfully!')
    return redirect(url_for('main.supervisors', role=current_user.role))

@main.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        supervisor_id = request.form.get('supervisor_id')
        job = Job(title=title, description=description, supervisor_id=supervisor_id)
        user.db.session.add(job)
        user.db.session.commit()
        flash('Job added successfully!')
    jobs = Job.query.all()
    supervisors = Supervisor.query.all()
    return render_template('jobs.html', jobs=jobs, supervisors=Supervisor.query.all(), role=current_user.role)

@main.route('/jobs/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    job = Job.query.get_or_404(id)
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        user.db.session.commit()
        flash('Job updated successfully!')
        return redirect(url_for('main.jobs'))
    return render_template('edit_job.html', job=job, role=current_user.role)

@main.route('/jobs/delete/<int:id>', methods=['POST'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    user.db.session.delete(job)
    user.db.session.commit()
    flash('Job deleted successfully!')
    return redirect(url_for('main.jobs', role=current_user.role))

@main.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        description = request.form.get('description')
        status = request.form.get('status')
        duration = int(request.form.get('duration'))  # Assume duration is posted as minutes
        duration_unit = request.form.get('duration_unit')
        difficulty = request.form.get('difficulty')
        job_id = request.form.get('job_id')
        
        # Convert hours to minutes if necessary
        if duration_unit == 'hours':
            duration = duration * 60  # Convert hours to minutes

        task = Task(description=description, status=status, duration=duration, difficulty=difficulty, job_id=job_id)
        user.db.session.add(task)
        user.db.session.commit()
        flash('Task added successfully!')

    tasks = Task.query.all()
    jobs = Job.query.all()  # This line gets all jobs for the form select field
    return render_template('tasks.html', tasks=tasks, jobs=jobs, role=current_user.role)

@main.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required  # Assuming you want these routes to be protected
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        duration = request.form.get('duration')
        if duration and duration.isdigit():
            task.duration = int(duration)
        else:
            flash('Invalid duration value. Please enter a valid number.')
            return redirect(url_for('main.edit_task', id=id))
        task.difficulty = request.form.get('difficulty')
        user.db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('main.tasks', role=current_user.role))
    
    jobs = Job.query.all()  # Get jobs for the dropdown in the edit form
    return render_template('edit_task.html', task=task, jobs=jobs)

@main.route('/tasks/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    user.db.session.delete(task)
    user.db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('main.tasks', role=current_user.role))