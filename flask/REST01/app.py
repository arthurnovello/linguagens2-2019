from flask import Flask, jsonify, request


lista = [{"id": 0, "nome": "pringles", "preco": 15.47}]


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
    return jsonify(item), 201


@app.route('/produto/<int:id>', methods=['GET'])
def get_produto(id):
    for produto in lista:
        if (produto['id'] == id):
            return jsonify(produto)
    return jsonify({'id': 'none'}), 404


if __name__ == "__main__":
    app.run(debug=True)
