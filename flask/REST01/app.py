from flask import Flask, jsonify, request


lista = [{"id": "0", "nome": "pringles", "preco": 15.47}]


app = Flask(__name__)


@app.route('/produtos', methods=['GET'])
def get_produtos():
    resp = {"produtos": lista}
    return jsonify(resp)


@app.route('/produto/<int:id>', methods=['POST'])
def post_produtos(id):
    data = request.get_json()
    item = {"id": id, "nome": data["nome"], "preco": data["preco"]}
    lista.append(item)
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=True)
