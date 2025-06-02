from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

from app.config.settings import Settings
from app.api.routes.token import init_auth_routes_token 
from app.api.routes.producao_route import init_auth_routes_token_producao
from app.api.routes.comercializacao_route import init_auth_routes_token_comercializacao
from app.api.routes.processamento_route import init_auth_routes_token_processamento
from app.api.routes.importacao_route import init_auth_routes_token_importacao
from app.api.routes.exportacao_route import init_auth_routes_token_exportacao

def create_app():
    """Factory principal da aplicação Flask"""
    conf = Settings()
    app = Flask(__name__)
    app.config.from_object(conf)
    
    # Configuração do Swagger
    app.config['SWAGGER'] = {
        'title': 'Tech Challenge – Fase 1 | Machine Learning Engineering - API de Dados Vitivinícolas da Embrapa',
        'uiversion': 3,
        'specs_route': '/apidocs/',
        'specs': [{
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }]
    }
    Swagger(app)

    # Inicialização de rotas
    init_auth_routes_token(app)
    init_auth_routes_token_producao(app)
    init_auth_routes_token_comercializacao(app)
    init_auth_routes_token_processamento(app)
    init_auth_routes_token_importacao(app)
    init_auth_routes_token_exportacao(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)