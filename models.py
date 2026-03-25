import uuid
from db import db

class Pagamento(db.Model):
    __tablename__ = "post"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(100), nullable=False, unique=False)
    valor_total = db.Column(db.Integer, nullable=False, unique=False)
    tipo_pagamento = db.Column(db.String(120), nullable=False, unique=False)
    numero_parcelas = db.Column(db.Integer, nullable=False)
    valor_parcela = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime)
    id_usuario = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)