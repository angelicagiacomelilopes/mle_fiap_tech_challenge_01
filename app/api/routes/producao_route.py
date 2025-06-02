# app/api/routes/producao.py
from flask import jsonify, request
from app.config.settings import Settings
from app.infra.auth.token import Token  
from app.infra.service.producao_service import ProducaoService
from app.dto.producao_dto import ProducaoRequestDTO
from pydantic import ValidationError
from flasgger import swag_from

def init_auth_routes_token_producao(app):
    config = Settings()
    token = Token(config)   
    producao = ProducaoService()    

    @app.route('/producao/health', methods=['GET'])
    def health_producao():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Produção
        responses:
          200:
            description: Serviço está funcionando
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rota Producao Funcionando corretamente"
        """
        return jsonify({"message": "Rota Producao Funcionando corretamente"})

    @app.route('/producao', methods=['GET'])
    @token.token_required
    @swag_from('doc/producao/get_producao.yaml')
    def get_producao_ano():
        try:
            # Validar o payload com o DTO
            request_data = request.get_json(force=True) if request.data else {}
            request_dto = ProducaoRequestDTO(**request_data)
            
            # Obter os dados validados do DTO
            filtros = {
                'ano': request_dto.ano,
                'produto': request_dto.produto,
                'categoria': request_dto.categoria
            }
            
            # Chamar o serviço com os filtros validados
            json_data = producao.get_data(**filtros)
            
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