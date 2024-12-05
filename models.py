from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicialização do Flask e SQLAlchemy

db = SQLAlchemy()

# Modelo de Usuário (User)
class User(db.Model):
    __tablename__ = 'TAB_USER'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Gera hash para a senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica a senha fornecida com o hash armazenado."""
        return check_password_hash(self.password_hash, password)


class Categoria(db.Model):
    __tablename__ = 'CATEGORIA'
    id = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(50), nullable=False, unique=True)

    # Relacionamento com Produto
    produtos = db.relationship('Produto', back_populates='categoria')


class Fornecedor(db.Model):
    __tablename__ = 'FORNECEDOR'
    id = db.Column(db.Integer, primary_key=True)
    nome_fornecedor = db.Column(db.String(50), nullable=False)
    telefone_fornecedor = db.Column(db.String(14), unique=True, nullable=False)
    email_fornecedor = db.Column(db.String(80), unique=True, nullable=False)
    # Relacionamento com Produto
    produtos = db.relationship('Produto', back_populates='fornecedor')


class Produto(db.Model):
    __tablename__ = 'PRODUTO'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)  # Defina a quantidade do produto
    validade = db.Column(db.Date, nullable=False)

    # Relacionamentos
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('FORNECEDOR.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('CATEGORIA.id'), nullable=False)

    fornecedor = db.relationship('Fornecedor', back_populates='produtos')
    categoria = db.relationship('Categoria', back_populates='produtos')

    # Relacionamento com Movimentacao
    movimentacoes = db.relationship('Movimentacao', back_populates='produto')

# Modelo de Funcionário
class Funcionario(db.Model):
    __tablename__ = 'FUNCIONARIO'
    id_funcionario = db.Column(db.Integer, primary_key=True)
    nome_funcionario = db.Column(db.String(50), nullable=False)
    cpf_funcionario = db.Column(db.String(14), unique=True, nullable=False)  # Considere mascarar
    email_funcionario = db.Column(db.String(80), unique=True, nullable=False)
    telefone_funcionario = db.Column(db.String(14))  # Validação pode ser adicionada
    cargo_funcionario = db.Column(db.String(50), nullable=False)


class Movimentacao(db.Model):
    __tablename__ = 'MOVIMENTACAO'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # "entrada" ou "saida"
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)  # Mudado para DateTime
    id_produto = db.Column(db.Integer, db.ForeignKey('PRODUTO.id'))

    produto = db.relationship('Produto', back_populates='movimentacoes')

    def save(self):
        """Valida e salva movimentações no estoque"""
        if self.tipo == 'saida' and self.produto.quantidade_estoque < self.quantidade:
            raise ValueError('Estoque insuficiente para a saída')
        self.produto.quantidade_estoque += self.quantidade if self.tipo == 'entrada' else -self.quantidade
        db.session.add(self)
        db.session.commit()

