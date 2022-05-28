from flask import request
from flask_restplus import Resource
from loguru import logger

from service.service.main_service import VaderService
from service.restplus import api, objResponse
from service.constants import mensagens, codeHttp
from service.util import doc_swagger

pa = api.namespace("")


@pa.route('/main', methods=['POST'])
class MainService(Resource):

    @api.expect(doc_swagger.INPUT_MAIN_SERVICE)
    def post(self) -> dict:
        try:
            dados_request = request.get_json()
            main_service = VaderService()
            resp = main_service.executar_rest(dados_request)
            response = objResponse.send_success(data=resp, messages=mensagens.SUCESSO_PREDICT, status=codeHttp.SUCCESS_200)

        except OSError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_OS, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)

        except TypeError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)

        except Exception as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_GENERIC, status=codeHttp.ERROR_500)
            logger.error(error)

        return response
