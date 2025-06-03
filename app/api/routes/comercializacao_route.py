# app/api/routes/producao.py
from flask import jsonify, request
from app.config.settings import Settings
from app.infra.auth.token_service import Token  
from app.infra.service.comercializacao_service import ComercializacaoService
from app.dto.comercializacao_dto import ComercializacaoRequestDTO
from pydantic import ValidationError
from flasgger import swag_from

def init_auth_routes_token_comercializacao(app):
    config = Settings()
    token = Token(config)   
    comercializacao = ComercializacaoService()    

    @app.route('/comercializacao/health', methods=['GET'])
    def health_comercializacao():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Comercialização
        responses:
          200:
            description: Serviço está funcionando
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rota Comercializacao Funcionando corretamente"
        """
        return jsonify({"message": "Rota Comercializacao Funcionando corretamente"})

    @app.route('/comercializacao', methods=['GET'])
    @token.token_required
    @swag_from('doc/comercializacao/get_comercializacao.yaml')
    def get_comercializacao_ano():
        """
        Endpoint principal de comercialização
        ---
        """
        try:
            # Validar o payload com o DTO
            request_data = request.get_json(force=True) if request.data else {}
            request_dto = ComercializacaoRequestDTO(**request_data)
            
            # Obter os dados validados do DTO
            filtros = {
                'ano': request_dto.ano,
                'produto': request_dto.produto,
                'categoria': request_dto.categoria
            }
            
            # Chamar o serviço com os filtros validados
            json_data = comercializacao.get_data(**filtros)
            
            return jsonify(json_data)
            
        except ValidationError as e:
            # Retornar erros de validação de forma detalhada
            errors = e.errors()
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in errors]
            return jsonify({
                "error": "Dados inválidos",
                "details": error_messages
            }), 400
            
        except Exception as e:
            return jsonify({
                "error": "Erro interno no servidor",
                "message": str(e)
            }), 500