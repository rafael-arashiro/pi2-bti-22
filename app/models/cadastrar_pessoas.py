from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class Cadastrar_pessoa(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    telefone = IntegerField("telefone", validators=[DataRequired()])
    admin = BooleanField("admin")

class Apagar_pessoa(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])