# app/api/routes/producao.py
from flask import jsonify, request
from app.config.settings import Settings
from app.infra.auth.token_service import Token  
from app.infra.service.importacao_service import ImportacaoService
from app.dto.importacao_dto import ImportacaoRequestDTO
from pydantic import ValidationError
from flasgger import swag_from

def init_auth_routes_token_importacao(app):
    config = Settings()
    token = Token(config)   
    importacao = ImportacaoService()    

    @app.route('/importacao/health', methods=['GET'])
    def health_importacao():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Importação
        responses:
          200:
            description: Serviço está funcionando
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rota importacao Funcionando corretamente"
        """
        return jsonify({"message": "Rota importacao Funcionando corretamente"})

    @app.route('/importacao', methods=['GET'])
    @token.token_required
    @swag_from('doc/importacao/get_importacao.yaml')
    def get_importacao_ano():
        """
        Endpoint para obter dados de importação
        
        """
        try:
            # Validar o payload com o DTO
            request_data = request.get_json(force=True) if request.data else {}
            
            request_dto = ImportacaoRequestDTO(**request_data)
           
            # Obter os dados validados do DTO
            filtros = {
                'year': request_dto.ano,
                'tipo': request_dto.tipo,
                'pais': request_dto.pais
            }
            
            # Chamar o serviço com os filtros validados
           
            json_data = importacao.get_data(**filtros)
            
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