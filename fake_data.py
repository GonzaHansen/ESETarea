from app import app, db
from app.models import User, Jobs, Application
from faker import Faker
from datetime import date
import random

fake = Faker('es_ES')

def generate_fake_users(count=10):
    with app.app_context():  # Activa el contexto de la aplicación Flas
        for _ in range(count):
            user = User(username=fake.user_name(), 
                        usertype=random.choice(['Alumno', 'Compañía']), 
                        email=fake.email(), 
                        password=random.choice(['pass12345']))
            db.session.add(user)
        db.session.commit()

def generate_fake_jobs(count=10):
    with app.app_context():  # Activa el contexto de la aplicación Flask
        for _ in range(count):
            job = Jobs(title=fake.job(), 
                       company=fake.company(), 
                       industry=random.choice(['Construcción', 'Tecnología', 'Software', 'Minería']), 
                       description=fake.text(), 
                       date_posted=date.today(),
                       link=fake.url(),
                       user_id=random.randint(1, User.query.count())) # Asigna un usuario aleatorio a cada trabajo
            db.session.add(job)
        db.session.commit()

def generate_fake_applications(count=10):
    with app.app_context():  # Activa el contexto de la aplicación Flask
        for _ in range(count):
            application = Application(gender=random.choice(['Masculino', 'Femenino', 'Otro']), 
                                      date_posted=date.today(), 
                                      degree=random.choice(['eSchool', 'dHighSchool', 'cBachelor', 'bMaster', 'aPHD']), 
                                      industry=random.choice(['Construction', 'Education', 'Food And Beverage', 'Pharmaceutical', 'Entertainment']), 
                                      experience=random.randint(1, 30), 
                                      cv=random.choice(['CV/Amanda Florez.pdf','CV/Carla Guiterrez.pdf','CV/Cristina Rodriguez.pdf','CV/Jaime Perez.pdf','CV/Mario Lopez.pdf','CV/Sofia Hernandez.pdf'
                                      , 'CV/asd.pdf', 'CV/Lisandro Perez.pdf']),  # Ruta a los archivos PDF en tu directorio static
                                      cover_letter=fake.text(), 
                                      user_id=random.randint(1, User.query.count()), # Asigna un usuario aleatorio a cada solicitud de empleo
                                      job_id=random.randint(1, Jobs.query.count())) # Asigna un trabajo aleatorio a cada solicitud de empleo
            db.session.add(application)
        db.session.commit()

if __name__ == '__main__':
    generate_fake_users()
    generate_fake_jobs()
    generate_fake_applications()
