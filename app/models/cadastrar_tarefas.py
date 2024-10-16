from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired

class Cadastrar_tarefa(FlaskForm):
    tarefa = StringField("tarefa", validators=[DataRequired()])
    local = StringField("local")
    data = DateField("data", validators=[DataRequired()])
    hora = TimeField("hora")

class Atualizar_tarefa(FlaskForm):
    tarefa = SelectField("tarefa_id", validators=[DataRequired()])
    local = StringField("local")
    data = DateField("data", validators=[DataRequired()])
    hora = TimeField("hora")


class Alocar_pessoa(FlaskForm):
    pessoa_id = SelectField("pessoa_id", validators=[DataRequired()])
    tarefa_id = SelectField("tarefa_id", validators=[DataRequired()])

class Apagar_tarefa(FlaskForm):
    tarefa_id = SelectField("tarefa_id", validators=[DataRequired()])
