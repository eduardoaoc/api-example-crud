from flask import Flask, jsonify
from flask_restful import  Api
from blacklist import BLACKLIST
from resource.hotel import *
from resource.usuario import *
from flask_jwt_extended import JWTManager


app= Flask(__name__)
#configuração do caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///banco.db'
app.config['SQLCHEMY_TRACK_MODIFICATIONS']= False
#Chave de autenticação
app.config['JWT_SECRET_KEY']= 'DontTell'
app.config['JWT_BLACKLIST_ENABLED']= True

api= Api(app)
jwt= JWTManager(app)

#Depois da primeira requisição cria banco.
@app.before_first_request
def cria_banco():
    banco.create_all()

@app.route('/')
def index():
    return {'status':'running'}

#verifica se ta na black list
@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'Message':'You have been logged out.'}), 401 
    #jsonify converte o dicionário para jason





#adiciona o recurso e escolhe o endereço de onde quer ser chamado (link)
api.add_resource(Hoteis, '/hoteis') 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') 
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
     