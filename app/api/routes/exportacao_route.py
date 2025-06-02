# app/api/routes/producao.py
from flask import jsonify, request
from app.config.settings import Settings
from app.infra.auth.token import Token  
from app.infra.service.exportacao_service import ExportacaoService
from app.dto.exportacao_dto import ExportacaoRequestDTO
from pydantic import ValidationError
from flasgger import swag_from

def init_auth_routes_token_exportacao(app):
    config = Settings()
    token = Token(config)   
    exportacao = ExportacaoService()    

    @app.route('/exportacao/health', methods=['GET'])
    def health_exportacao():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Exportação
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
        return jsonify({"message": "Rota exportacao Funcionando corretamente"})

    @app.route('/exportacao', methods=['GET'])
    @token.token_required
    @swag_from('doc/exportacao/get_exportacao.yaml')
    def get_exportacao_ano():
        try:
            # Validar o payload com o DTO
            request_data = request.get_json(force=True) if request.data else {}
            
            request_dto = ExportacaoRequestDTO(**request_data)
           
            # Obter os dados validados do DTO
            filtros = {
                'year': request_dto.ano,
                'tipo': request_dto.tipo,
                'pais': request_dto.pais
            }
            
            # Chamar o serviço com os filtros validados
           
            json_data = exportacao.get_data(**filtros)
            
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