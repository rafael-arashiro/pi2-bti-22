from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired

class Cadastrar_tarefa(FlaskForm):
    tarefa = StringField("tarefa", validators=[DataRequired()])
    local = StringField("local")
    data = DateField("data", validators=[DataRequired()])
    dataFinal = DateField("dataFinal", validators=[DataRequired()])
    segunda = BooleanField("segunda")
    terca = BooleanField("terca")
    quarta = BooleanField("quarta")
    quinta = BooleanField("quinta")
    sexta = BooleanField("sexta")
    sabado = BooleanField("sabado")
    domingo = BooleanField("domingo")
    hora = TimeField("hora")

class Importar_tarefas(FlaskForm):
    arquivo = FileField("arquivo", validators=[DataRequired()])

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
