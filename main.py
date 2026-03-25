from flask import Flask, request, jsonify
from db import db
from models import Pagamento
import os
from datetime import datetime
import requests

postgres_user = os.environ.get('POSTGRES_USER', 'appuser')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'apppass')
postgres_url = os.environ.get('POSTGRES_URL', 'localhost')
validador_url = os.environ.get('VALIDADOR_URL' 'validador_url')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_url}:5432/post"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/pagamento", methods=["POST"])
def create_pagamento():
    data = request.json

    response = requests.get(f"http://{validador_url}/users/{data["id_usuario"]}")

    if response.status_code == 404:
        raise Exception("Usuário não encontrado!")

    pagamento = Pagamento(
        codigo=data["codigo"],
        valor_total=data["valor_total"],
        tipo_pagamento=data["tipo_pagamento"],
        numero_parcelas=data["numero_parcelas"],
        valor_parcela=data["valor_total"] / data["numero_parcelas"],
        id_usuario=data["id_usuario"],
        data=datetime.now()
    )

    db.session.add(pagamento)
    db.session.commit()

    return jsonify({
        "id": str(pagamento.id),
        "codigo": pagamento.codigo,
        "valor_total": pagamento.valor_total,
        "tipo_pagamento": pagamento.tipo_pagamento,
        "numero_parcelas": pagamento.numero_parcelas,
        "valor_parcela": pagamento.valor_parcela,
        "data": pagamento.data,
        "id_usuario": pagamento.id_usuario
    }), 201

@app.route("/pagamento", methods=["GET"])
def list_pagamentos():
    pagamentos = Pagamento.query.all()

    return [
        {
            "id": str(pagamento.id),
            "codigo": pagamento.codigo,
            "valor_total": pagamento.valor_total,
            "tipo_pagamento": pagamento.tipo_pagamento,
            "numero_parcelas": pagamento.numero_parcelas,
            "valor_parcela": pagamento.valor_parcela,
            "data": pagamento.data,
            "id_usuario": pagamento.id_usuario
        }
        for pagamento in pagamentos
    ], 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

@app.route("/pagamento/<uuid:pagamento_id>", methods=["DELETE"])
def delete_pagamentos(pagamento_id):
    pagamento = Pagamento.query.get_or_404(pagamento_id)

    db.session.delete(pagamento)
    db.session.commit()

    return "", 204