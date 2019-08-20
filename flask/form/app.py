from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/meuform', methods=['POST'])
def meuform():
    nome = request.form['nome']
    address = request.form['end']
    email = request.form['email']

    resp = {'nome': nome,
            'end': address,
            'email': email}
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True)
