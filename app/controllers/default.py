from app import app
from flask import render_template, redirect, url_for, session, request
from jinja2 import Environment, FileSystemLoader
from app.models.formulario import Login
from app.models.cadastrar_pessoas import Cadastrar_pessoa, Apagar_pessoa, Atualizar_pessoa
from app.models.cadastrar_tarefas import Cadastrar_tarefa, Apagar_tarefa, Alocar_pessoa, Atualizar_tarefa
import mysql.connector

def defLocal(localDb):
    local = ""
    for letra in localDb:
        if letra == " ":
            local = local + "+"
        else:
            local = local + str(letra)
    return local

env = Environment(loader=FileSystemLoader('templates'))
env.globals['defLocal'] = defLocal

mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

@app.route("/", methods=["GET", "POST"])
def index():
    formulario = Login()
    return render_template("index.html", formulario=formulario)

@app.route("/login", methods=["GET", "POST"])
def login():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    formulario = Login()
    my_cursor = mydb.cursor()

    if formulario.validate_on_submit():
        nome = formulario.nome.data
        password = formulario.password.data
        my_cursor.execute('SELECT * FROM pessoas WHERE Nome=%s AND Senha=%s', (nome, password))
        record = my_cursor.fetchone()
        if record:
            session['loggedin']=True
            session['nome']=record[1]
            session['admin']=record[4]
            return redirect(url_for("entrada"))
    else:
        return redirect(url_for("index"))

    mydb.close()

    return index()

@app.route("/logout", methods=["GET", "POST"])
def logout():

    session['loggedin']=False
    session['nome']=''
    session['admin']=''

    return index()

@app.route("/entrada")
def entrada():

    if session['loggedin']:
        pass
    else:
        return redirect(url_for("index"))

    return render_template("entrada.html", nome=session['nome'], admin=session['admin'])

@app.route("/cadastrar_pessoas")
def cadastrar_pessoas():

    if session['loggedin']:
        pass
    else:
        return redirect(url_for("index"))

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    cadastro_pessoa = Cadastrar_pessoa()
    atualizar_pessoa = Atualizar_pessoa()
    apagar_pessoa = Apagar_pessoa()

    cursor = mydb.cursor()
    cursor.execute("SELECT Nome FROM pessoas")
    listadenomes = cursor.fetchall()
    atualizar_pessoa.nome.choices = []
    for nome in listadenomes:
        if len(listadenomes) <= 0:
            pass
        else:
            item = nome[0]
            atualizar_pessoa.nome.choices.append(item)

    cursorDois = mydb.cursor()
    cursorDois.execute("SELECT Nome FROM pessoas")
    listadenomes = cursorDois.fetchall()
    apagar_pessoa.pessoa_id.choices = []
    for nome in listadenomes:
        if len(listadenomes) <= 0:
            pass
        else:
            item = nome[0]
            apagar_pessoa.pessoa_id.choices.append(item)

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()

    mydb.close()

    return render_template("cadastrar_pessoas.html", nome=session['nome'], cadastro_pessoa=cadastro_pessoa, atualizar_pessoa=atualizar_pessoa, apagar_pessoa=apagar_pessoa, grupoPessoas=grupoPessoas)

@app.route("/cadastroPessoa", methods=["GET", "POST"])
def cadastroPessoa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    cadastro_pessoa = Cadastrar_pessoa()

    nome = cadastro_pessoa.nome.data
    password = cadastro_pessoa.password.data
    telefone = cadastro_pessoa.telefone.data
    admin = cadastro_pessoa.admin.data

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO pessoas (Nome,Senha,Telefone,admin) VALUES ('{nome}','{password}',{telefone},{admin}) ON DUPLICATE KEY UPDATE Senha = '{password}', Telefone = {telefone}, admin = {admin}"

    my_cursor.execute(sql)
    mydb.commit()
    
    mydb.close()

    return cadastrar_pessoas()

@app.route("/atualizarPessoa", methods=["GET", "POST"])
def atualizarPessoa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    atualizar_pessoa = Atualizar_pessoa()

    nome = atualizar_pessoa.nome.data
    password = atualizar_pessoa.password.data
    telefone = atualizar_pessoa.telefone.data
    admin = atualizar_pessoa.admin.data

    my_cursor = mydb.cursor()

    sql = f"UPDATE pessoas SET Senha = '{password}', Telefone = {telefone}, admin = {admin} WHERE Nome='{nome}'"

    my_cursor.execute(sql)
    mydb.commit()
    
    mydb.close()

    return cadastrar_pessoas()

@app.route("/apagarPessoa", methods=["GET", "POST"])
def apagarPessoa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    apagar_pessoa = Apagar_pessoa()

    pessoa_id = apagar_pessoa.pessoa_id.data

    my_cursor_associado = mydb.cursor()

    sql = f"DELETE FROM pessoas_tarefas WHERE pessoa_id = (SELECT id FROM pessoas WHERE Nome = '{pessoa_id}')"

    my_cursor_associado.execute(sql)
    mydb.commit()

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM pessoas WHERE Nome='{pessoa_id}'"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_pessoas()

@app.route("/cadastrar_tarefas")
def cadastrar_tarefas():

    if session['loggedin']:
        pass
    else:
        return redirect(url_for("index"))

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    cadastro_tarefa = Cadastrar_tarefa()

    pessoas_tarefas = Alocar_pessoa()

    atualizar_tarefa = Atualizar_tarefa()

    apagar_tarefa = Apagar_tarefa()
    
    my_cursor_pessoas_tarefas_um = mydb.cursor()
    my_cursor_pessoas_tarefas_um.execute("SELECT tarefas FROM tarefas")
    listadetarefas = my_cursor_pessoas_tarefas_um.fetchall()
    atualizar_tarefa.tarefa.choices = []
    for nome in listadetarefas:
        if len(listadetarefas) <= 0:
            pass
        else:
            item = nome[0]
            atualizar_tarefa.tarefa.choices.append(item)

    cursor = mydb.cursor()
    cursor.execute("SELECT Nome FROM pessoas")
    listadenomes = cursor.fetchall()
    pessoas_tarefas.pessoa_id.choices = []
    for nome in listadenomes:
        if len(listadenomes) <= 0:
            pass
        else:
            item = nome[0]
            pessoas_tarefas.pessoa_id.choices.append(item)

    my_cursor_pessoas_tarefas_dois = mydb.cursor()
    my_cursor_pessoas_tarefas_dois.execute("SELECT tarefas FROM tarefas")
    listadetarefas = my_cursor_pessoas_tarefas_dois.fetchall()
    pessoas_tarefas.tarefa_id.choices = []
    for nome in listadetarefas:
        if len(listadetarefas) <= 0:
            pass
        else:
            item = nome[0]
            pessoas_tarefas.tarefa_id.choices.append(item)
    
    my_cursor_pessoas_tarefas_tres = mydb.cursor()
    my_cursor_pessoas_tarefas_tres.execute("SELECT tarefas FROM tarefas")
    listadetarefas = my_cursor_pessoas_tarefas_tres.fetchall()
    apagar_tarefa.tarefa_id.choices = []
    for nome in listadetarefas:
        if len(listadetarefas) <= 0:
            pass
        else:
            item = nome[0]
            apagar_tarefa.tarefa_id.choices.append(item)
    print(apagar_tarefa.tarefa_id.choices)

    my_cursor_tarefas = mydb.cursor()
    my_cursor_tarefas.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, DATE_FORMAT (tarefas.data,"%d/%m/%Y"), tarefas.hora FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id ORDER BY id')

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    return render_template("cadastrar_tarefas.html", nome=session['nome'], cadastro_tarefa=cadastro_tarefa, pessoas_tarefas=pessoas_tarefas, apagar_tarefa=apagar_tarefa, grupoTarefas=grupoTarefas,  defLocal=defLocal, atualizar_tarefa=atualizar_tarefa)

@app.route("/cadastroTarefa", methods=["GET", "POST"])
def cadastroTarefa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    cadastro_tarefa = Cadastrar_tarefa()

    tarefa = cadastro_tarefa.tarefa.data
    local = cadastro_tarefa.local.data
    data = cadastro_tarefa.data.data
    hora = cadastro_tarefa.hora.data

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO tarefas (tarefas,local,data,hora) VALUES ('{tarefa}','{local}','{data}','{hora}') ON DUPLICATE KEY UPDATE local = '{local}', data = '{data}', hora = '{hora}'"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/pessoaTarefa", methods=["GET", "POST"])
def pessoaTarefa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    pessoas_tarefas = Alocar_pessoa()

    pessoa_id = pessoas_tarefas.pessoa_id.data
    tarefa_id = pessoas_tarefas.tarefa_id.data

    my_cursor = mydb.cursor()

    if request.form["direcionar"] == "colocar":
        sql = f"INSERT INTO pessoas_tarefas VALUES ((SELECT id FROM pessoas WHERE Nome = '{pessoa_id}'),(SELECT id FROM tarefas WHERE tarefas = '{tarefa_id}')) ON DUPLICATE KEY UPDATE pessoa_id = pessoa_id"
        my_cursor.execute(sql)
    elif request.form["direcionar"] == "tirar":
        sql = f"DELETE FROM pessoas_tarefas WHERE pessoa_id = (SELECT id FROM pessoas WHERE Nome = '{pessoa_id}') AND tarefa_id = (SELECT id FROM tarefas WHERE tarefas = '{tarefa_id}')"
        my_cursor.execute(sql)
    else:
        pass

    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/atualizarTarefa", methods=["GET", "POST"])
def atualizarTarefa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    atualizar_tarefa = Atualizar_tarefa()

    tarefa = atualizar_tarefa.tarefa.data
    local = atualizar_tarefa.local.data
    data = atualizar_tarefa.data.data
    hora = atualizar_tarefa.hora.data

    my_cursor = mydb.cursor()

    sql = f"UPDATE tarefas SET local = '{local}', data = '{data}', hora = '{hora}' WHERE tarefas = '{tarefa}'"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/apagarTarefa", methods=["GET", "POST"])
def apagarTarefa():

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    apagar_tarefa = Apagar_tarefa()

    tarefa_id = apagar_tarefa.tarefa_id.data

    my_cursor_associado = mydb.cursor()

    sql = f"DELETE FROM pessoas_tarefas WHERE tarefa_id = (SELECT id FROM tarefas WHERE tarefas = '{tarefa_id}')"

    my_cursor_associado.execute(sql)
    mydb.commit()

    my_cursor = mydb.cursor()

    sql = f"DELETE FROM tarefas WHERE tarefas = '{tarefa_id}'"

    my_cursor.execute(sql)
    mydb.commit()

    mydb.close()

    return cadastrar_tarefas()

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():

    if session['loggedin']:
        pass
    else:
        return redirect(url_for("index"))

    nome=session['nome']

    mydb = mysql.connector.connect(host='localhost',user='root',password='Ihc741258_',database='pi_db')

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM pessoas')

    grupoPessoas = my_cursor.fetchall()

    my_cursor_tarefas_admin = mydb.cursor()
    my_cursor_tarefas_admin.execute('SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, DATE_FORMAT (tarefas.data,"%d/%m/%Y"), tarefas.hora, pessoas.Telefone FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id')

    grupoTarefasAdmin = my_cursor_tarefas_admin.fetchall()

    my_cursor_tarefas = mydb.cursor()
    sql = f"SELECT tarefas.id, tarefas.tarefas, pessoas.Nome, tarefas.local, tarefas.data, tarefas.hora FROM tarefas, pessoas INNER JOIN pessoas_tarefas WHERE tarefas.id=pessoas_tarefas.tarefa_id AND pessoas.id=pessoas_tarefas.pessoa_id AND pessoas.id=(SELECT id FROM pessoas WHERE Nome = '{nome}')"
    my_cursor_tarefas.execute(sql)

    grupoTarefas = my_cursor_tarefas.fetchall()

    mydb.close()

    grupoTarefasAdminComMensagem = []

    for tarefa in grupoTarefasAdmin:
        mensagem = "Olá,%20Voluntário%20Ágape!%20Tudo%20bem?%20Este%20é%20um%20lembrete%20de%20que%20contamos%20com%20você%20na%20escala%20de%20" + str(tarefa[1]) + ",%20no%20próximo%20dia%20" + str(tarefa[4]) + ",%20" + str(tarefa[5]) + ".%20Agradecemos%20muito%20sua%20dedicação%20e%20participação!%20Local:%20" + str(tarefa[3])
        if len(grupoTarefasAdmin) <= 0:
            pass
        else:
            lista = list(tarefa)
            lista.insert(7, mensagem)
            lista.insert(8, mensagem)
            tupla = tuple(lista)
            grupoTarefasAdminComMensagem.append(tupla)

    return render_template("relatorio.html", nome=session['nome'], admin=session['admin'], grupoPessoas=grupoPessoas, grupoTarefasAdminComMensagem=grupoTarefasAdminComMensagem, grupoTarefas=grupoTarefas, defLocal=defLocal)

