# data/data_fetcher.py

import quandl
import requests
import numpy as np
from datetime import datetime, timedelta

class DataFetcher:

    API_ENDPOINT = "https://www.quandl.com/api/v3/datasets/LBMA/GOLD/data.json"

    def __init__(self, callback):
        self.ultima_chamada = None
        self.contagem_chamadas = 0
        self.api_key = quandl.ApiConfig.api_key  # Considere movê-la para um arquivo de configuração ou variável de ambiente
        self.callback = callback

    def calculate_rows(self, interval):
        interval_rows = {
            "7d": 7, 
            "30d": 30, 
            "365d": 365, 
            "all": 10000
        }
        return interval_rows.get(interval, 1)

    def _can_make_api_call(self):
        if self.ultima_chamada is None:
            self.ultima_chamada = datetime.now()
            return True
        
        diff_time = datetime.now() - self.ultima_chamada
        if diff_time > timedelta(minutes=5):
            self.contagem_chamadas = 0
            self.ultima_chamada = datetime.now()
            return True
        
        if self.contagem_chamadas < 30:
            return True
        return False

    def fetch_price(self, interval):
        if not self._can_make_api_call():
            raise ValueError("Você atingiu o limite de chamadas. Por favor, aguarde alguns minutos e tente novamente.")

        self.contagem_chamadas += 1

        rows = self.calculate_rows(interval)
        if not rows:
            raise ValueError("Não foi possível recuperar os dados para o intervalo selecionado.")
        
        response = requests.get(f"{self.API_ENDPOINT}?api_key={self.api_key}&limit={rows}")

        if response.status_code != 200:
            raise ValueError("Erro na requisição dos dados.")
        
        data = response.json()
        date, price = zip(*[(item[0], item[1]) for item in data["dataset_data"]["data"]])
        date = [np.datetime64(d) for d in date]

        self.callback(date, price)
        return date, price
