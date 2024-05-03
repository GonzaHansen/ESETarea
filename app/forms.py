from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from app.models import User
class RegistrationForm(FlaskForm):
    usertype = SelectField('Tipo de Usuario',
                           choices=[('Alumno', 'Alumno'),
                                    ('Compañía', 'Compañía')],
                           )
    username = StringField('Nombre de usuario',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    password = PasswordField('Contraseña')
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[EqualTo('password')])
    submit = SubmitField('Registrarse')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya se encuentra en uso. Por favor elige uno diferente.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya se encuentra en uso. Por favor elige uno diferente.')
class LoginForm(FlaskForm):
    usertype = SelectField('Tipo de Usuario',
                           choices=[('Alumno', 'Alumno'),
                                    ('Compañía', 'Compañía')],
                           )
    email = StringField('Email',
                        validators=[Email()])
    password = PasswordField('Contraseña')
    remember = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')


class ReviewForm(FlaskForm):
    username = StringField('Nombre')
    review = TextAreaField('Reseña')
    submit = SubmitField('Enviar Reseña')


class JobForm(FlaskForm):
    title = StringField('Cargo',
                        validators=[Length(min=2, max=20)])
    industry = SelectField('Industria', choices=[('Construcción', 'Construcción'),
                                                ('Tecnología', 'Tecnología'),
                                                ('Software', 'Software'),
                                                ('Minería', 'Minería')])
    description = TextAreaField('Descripción del cargo')
    link= StringField('Enlace empresa')
    submit = SubmitField('Crear')
class ApplicationForm(FlaskForm):
    gender = SelectField('Género', choices=[('Masculino', 'Masculino'),
                                            ('Femenino', 'Femenino'),
                                            ('Otro', 'Otro')],
                         default='masculino')
    degree = SelectField('Degree',
                         default='eSchool',
                         choices=[('eSchool', 'School'),
                                  ('dHighSchool', 'HighSchool'),
                                  ('cBachelor', 'Bachelor'),
                                  ('bMaster', 'Master'),
                                  ('aPHD', 'PHD')])
    industry = SelectField('Industria',
                           default='Construction',
                           choices=[('Construction', 'Construction'),
                                    ('Education', 'Education'),
                                    ('Food And Beverage', 'Food and Beverage'),
                                    ('Pharmaceutical', 'Pharmaceutical'),
                                    ('Entertainment', 'Entertainment'),
                                    ('Manufacturing', 'Manufacturing'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Agriculture', 'Agriculture'),
                                    ('Transportation', 'Transportation'),
                                    ('Computer And Technology', 'Computer and Technology'),
                                    ('Healthcare', 'Healthcare'),
                                    ('Media And News', 'Media and News'),
                                    ('Hospitality', 'Hospitality'),
                                    ('Energy', 'Energy'),
                                    ('Fashion', 'Fashion'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Finance and Economic', 'Finance and Economic'),
                                    ('Advertising And Marketing', 'Advertising and Marketing'),
                                    ('Mining', 'Mining'),
                                    ('Aerospace', 'Aerospace')])
    experience = IntegerField('Edad')
    cv = FileField('Subir CV', validators=[FileAllowed(['jpg', 'png', 'bmp','pdf'])])
    cover_letter = TextAreaField('Carta de presentación')
    submit = SubmitField('Enviar')