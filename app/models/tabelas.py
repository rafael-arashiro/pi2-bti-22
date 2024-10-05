from app import mydb

class Pessoas(mydb.Model):
    __tablename__ = "pessoas"
    
    id = mydb.Column(mydb.Integer, primary_key=True)
    nome = mydb.Column(mydb.String, unique=True)
    password = mydb.Column(mydb.String)
    telefone = mydb.Column(mydb.Integer, unique=True)
    
    def __init__(self, nome, password, telefone):
        self.nome = nome
        self.password = password
        self.telefone = telefone
        
    def __repr__(self):
        return "<User %r>" % self.username
    
class Tarefas(mydb.Model):
    __tablename__ = "tarefas"
    
    id = mydb.Column(mydb.Integer, primary_key=True)
    tarefas = mydb.Column(mydb.String)
    user_id = mydb.Column(mydb.Integer, mydb.ForeignKey('users.id'))
    
    user = mydb.relationship('User', foreign_keys=user_id)
    
    def __init__(self, tarefa, user_id):
        self.tarefa = tarefa
        self.user_id = user_id
        
    def __repr__(self):
        return "<Tarefa %r>" % self.id