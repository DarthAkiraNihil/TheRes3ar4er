from config import config
import requests


class LogDumper:
    def __init__(self):
        self.__token = config['log_dumper']['token']
        self.__chatId = config['log_dumper']['chat_id']


    def send(self, text):
        return requests.post(
            f'https://api.telegram.org/bot{self.__token}/sendMessage',
            data={
                'chat_id': self.__chatId,
                'text': text
            }
        )


