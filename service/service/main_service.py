import time
import json
from loguru import logger
from service.constants import mensagens
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class VaderService():

    def __init__(self):
        logger.debug(mensagens.INICIO_LOAD_SERVICO)
        self.load_model()

    def load_model(self):
        """"
        Carrega o modelo VADER a ser usado
        """

        self.model = SentimentIntensityAnalyzer()

        logger.debug(mensagens.FIM_LOAD_MODEL)

    def executar_rest(self, texts):
        response = {}

        logger.debug(mensagens.INICIO_PREDICT)
        start_time = time.time()

        response_predicts = self.buscar_predicao(texts['textoMensagem'])

        logger.debug(mensagens.FIM_PREDICT)
        logger.debug(f"Fim de todas as predições em {time.time()-start_time}")

        df_response = pd.DataFrame(texts, columns=['textoMensagem'])
        df_response['predict'] = response_predicts

        df_response = df_response.drop(columns=['textoMensagem'])

        response = {
                     "listaClassificacoes": json.loads(df_response.to_json(
                                                                            orient='records', force_ascii=False))}

        return response

    def buscar_predicao(self, texts):
        """
        Pega o modelo carregado e aplica em texts
        """
        logger.debug('Iniciando o predict...')

        response = []

        for text in texts:
            sentiment_dict = self.model.polarity_scores(text)

            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05:
                response.append("Positive")

            elif sentiment_dict['compound'] <= - 0.05:
                response.append("Negative")

            else:
                response.append("Neutral")

        return response