from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import requests


class PresenceAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.api_key = kwargs.get('secret_key')

    # Serve Levenshtein distance per 'misurare' le parole
    def can_process(self, statement):
        words = ['location', 'sede', 'sedi']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):

        # Make a request to the temperature API
        response = requests.get('https://apibot4me.imolinfo.it/v1/locations', headers={"api_key": self.api_key})
        data = response.json()

        # Let's base the confidence value on if the request was successful
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0

        if response.status_code == 200:
            strReturn = ""
            for record in response.json():
                strReturn += "\tNome Azienda: " + record.get('name', "non registrato") + '\n'
                strReturn += "\tOre fatturate: " + str(record.get('address', "non registrato")) + '\n'
                #strReturn += "\tLong: " + str(record.get('long', "non registrata")) + '\n'
                #strReturn += "\tLat: " + str(record.get('lat', "non registrata")) + '\n'
                strReturn += '\n'

        #temperature = data.get('name', 'unavailable')

        #response_statement = Statement(text='The current temperature is {}'.format(temperature))
        response_statement = Statement(strReturn)
        return response_statement