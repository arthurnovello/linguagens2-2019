from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "tiago": generate_password_hash("arroz"),
    "dobbin": generate_password_hash("rivotril"),
    "sergio": generate_password_hash("escapamento_novo")
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/')
def index():
    return '<h1>Area de livre acesso</h1>'


@app.route('/protegido1')
@auth.login_required
def prot1():
    return '<h1>Area protegida</h1>'


@app.route('/protegido2')
@auth.login_required
def prot2():
    return '<h1>Area protegida2'


if __name__ == "__main_":
    app.run(debug=True)
