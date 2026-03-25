import uuid
from db import db

class Pagamento(db.Model):
    __tablename__ = "pagamento"

    id_usuario = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), nullable=False, unique=True)