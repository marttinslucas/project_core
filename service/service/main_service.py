from pyexpat import model
import time
import json
from loguru import logger
from service.constants import mensagens
import pandas as pd
from googletrans import Translator

class translateService():

    def __init__(self):
        logger.debug(mensagens.INICIO_LOAD_SERVICO)
        self.load_model()

    def load_model(self):
        """"
        Carrega o modelo Translator a ser usado
        """

        self.model = Translator()

        logger.debug(mensagens.FIM_LOAD_MODEL)

    def executar_rest(self, texts):
        response = {}

        logger.debug(mensagens.INICIO_PREDICT)
        start_time = time.time()

        response_translate = self.buscar_traducao(texts['textoMensagem'])
        print(response_translate)

        logger.debug(mensagens.FIM_PREDICT)
        logger.debug(f"Fim de todas as traduções em {time.time()-start_time}")
        df_response = pd.DataFrame(texts, columns=['textoMensagem'])
        df_response['frase_portugues'] = response_translate

        df_response = df_response.drop(columns=['textoMensagem'])
        response = {
                     "fraseTraduzida": json.loads(df_response.to_json(
                                                                            orient='records', force_ascii=False))}
        return response

    def buscar_traducao(self, texts):
        """
        Pega o modelo carregado e aplica em texts
        """

        logger.debug('Iniciando o tradutor...')

        response = []
        for phrase in texts:
            translate_dict = self.model.translate(phrase, dest='pt')
            response.append(translate_dict.text)
        
        return response