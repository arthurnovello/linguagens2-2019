from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Navegação permitida!</h1>'


@app.route('/prot')
def prot1():

    auth = request.authorization

    if auth and auth.username == 'usr' and auth.password == 'pwd':
        return '<h1>Recurso valioso</h1>'

    return make_response('Tentativa sem Autenticação', 401,
                         {'WWW-Authenticate': 'Basic realm=""'})
    return '<h1>Acesso negado</h1>', 402


if __name__ == "__main__":
    app.run(debug=True)
