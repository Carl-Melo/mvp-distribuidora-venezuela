from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome_razao = db.Column(db.String(120), nullable=False)
    tipo_cliente = db.Column(db.String(20), nullable=False)
    telefone_whatsapp = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='ativo', nullable=False)

class Venda(db.Model):
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True)
    valor_venda = db.Column(db.Numeric(10, 2), nullable=False)
    custo_estimado = db.Column(db.Numeric(10, 2), nullable=False)
    lucro_liquido = db.Column(db.Numeric(10, 2), nullable=False)
    modalidade = db.Column(db.String(20), nullable=False)
    forma_pagamento = db.Column(db.String(30), nullable=False)
    status_pagamento = db.Column(db.String(20), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
