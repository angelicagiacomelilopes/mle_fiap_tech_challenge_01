# app/api/routes/producao.py
from flask import jsonify, request
from app.config.settings import Settings
from app.infra.auth.token import Token  
from app.infra.service.processamento_service import ProcessamentoService
from app.dto.processamento_dto import ProcessamentoRequestDTO
from pydantic import ValidationError
from flasgger import swag_from

def init_auth_routes_token_processamento(app):
    config = Settings()
    token = Token(config)   
    processamento = ProcessamentoService()    

    @app.route('/processamento/health', methods=['GET'])
    def health_processamento():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Processamento
        responses:
          200:
            description: Serviço está funcionando
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rota Processamento Funcionando corretamente"
        """
        return jsonify({"message": "Rota Processamento Funcionando corretamente"})

    @app.route('/processamento', methods=['GET'])
    @token.token_required
    @swag_from('doc/processamento/get_processamento.yaml')
    def get_processamento_ano():
        try:
            # Validar o payload com o DTO
            request_data = request.get_json(force=True) if request.data else {}
            
            request_dto = ProcessamentoRequestDTO(**request_data)
           
            # Obter os dados validados do DTO
            filtros = {
                'year': request_dto.ano,
                'tipo': request_dto.tipo,
                'subtipo': request_dto.subtipo,
                'cultivar': request_dto.cultivar
            }
            
            # Chamar o serviço com os filtros validados
           
            json_data = processamento.get_data(**filtros)
            
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