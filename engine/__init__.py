from .process import Process


class Bot:
    def __init__(self):
        self.__brain = Process()

    def say(self, phrase: str):
        print(phrase)

    def request_command(self, text: str='Enter a command:'):
        self.say(phrase=text)
        return input('R: ')

    def process(self, text):
        process = self.__brain.process(text=text)
        extra_data = None
        while True:
            if extra_data: data = process.send(extra_data)
            else: data = next(process)
            if 'alert' in data: 
                extra_data = self.request_command(text=data['alert'])
            if 'result' in data: return data['result']
