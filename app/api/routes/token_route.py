from app.infra.auth.token_service import Token
from app.config.settings import Settings
from flask import jsonify,request
from flasgger import swag_from

def init_auth_routes_token(app):
    """Registra rotas de autenticação no app Flask."""
    
    @app.route('/token/health', methods=['GET'])
    def health_token():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Token
        responses:
          200:
            description: Serviço está funcionando
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rota exportacao Funcionando corretamente"
        """
        return jsonify({"message": "Rota Tolken Funcionando corretamente"})
    
    @app.route("/login", methods=["POST"])
    @swag_from('doc/token/get_token.yaml')
    def login():
        config = Settings()
        token = Token(config)   

        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        
        if username == config.USERNAME and password == config.PASSWORD:
            token = token.create_token(username)
            return jsonify({"access_token": token})  
        return jsonify({"error": "Invalid credentials"}), 401

 

 


