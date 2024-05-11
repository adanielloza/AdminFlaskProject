# models/user.py
from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50), nullable=False)  # New role field
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<User {self.name}, Role {self.role}>'
    
    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)
        return result

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.filter(cls.id == id).first()
        print(user.id)
        return user

class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='supervisor')
    jobs = db.relationship('Job', backref='supervisor', lazy='dynamic')
    
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.id'))
    tasks = db.relationship('Task', back_populates='job')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    job = db.relationship('Job', back_populates='tasks')

   
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)





