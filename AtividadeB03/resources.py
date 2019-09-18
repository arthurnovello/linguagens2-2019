from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel, BolosModel, EncomendasModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('username', help='O campo dever ser preenchido',
                    required=True)
parser.add_argument('password', help='O campo dever ser preenchido',
                    required=True)


class UserRegistration(Resource):
    def post(self):
        parser.add_argument('nome', help='O campo dever ser preenchido',
                            required=True)
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already \
                    exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            nome=data['nome']
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t \
                    exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class AllBolos(Resource):
    def get(self):
        return BolosModel.return_all()


class Encomendar(Resource):
    @jwt_required
    def post(self):
        parser.add_argument('bolo_id', help='O campo dever ser preenchido',
                            required=True)
        parser.remove_argument('password')
        parser.remove_argument('nome')
        data = parser.parse_args()

        new_encomenda = EncomendasModel(
            usr_id=UserModel.find_by_username(data['username']).id,
            bolo_id=data['bolo_id'],
            preco=BolosModel.return_by_id(data['bolo_id']).preco
        )

        try:
            new_encomenda.save_to_db()
            return {
                'message': 'Encomenda was created'
            }
        except:
            return {'message': 'Something went wrong'}, 500


class Encomendas(Resource):
    @jwt_required
    def get(self):
        return EncomendasModel.return_all()

    @jwt_required
    def delete(self):
        return EncomendasModel.delete_by_id(id)


class Encomenda(Resource):
    @jwt_required
    def get(self, id):
        return EncomendasModel.return_by_id(id)
