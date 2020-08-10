import os, json, nltk, string, random
from importlib import import_module
from fuzzywuzzy import fuzz
from typing import Dict, Any, AnyStr, List, Callable, Generator
from . import modules
from .utils.exceptions import (
    ActionNotFoundException,
    ModuleNotConfiguredException,
)


class Process:
    APOLOGY_MESSAGES = ["Sorry, I didn't understant."]

    def __init__(self, *, config_dir:str=None):
        self.config_dir = config_dir or os.getenv(
            'CONFIG_PATH',
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        )
        self.config = self._get_config()

    def _get_config(self) -> Dict[str, Any]:
        path = os.path.join(self.config_dir, 'commands.json')
        
        with open(path, 'rb') as f: config = json.load(f)
        
        return config

    def _get_process_method(self, module:str) -> Callable:
        try:
            module = import_module(f'{modules.__package__}.{module}.main')
        except ModuleNotFoundError:
            raise ModuleNotConfiguredException(name=module)

        return module.process

    def _parse_user_input(self, text:str, only_params:bool=False) -> List[Any]:
        tokens = [
            word for word in nltk.word_tokenize(text.lower()) \
                if word not in string.punctuation
        ]

        return tokens if only_params else (tokens[0], tokens[1:])

    def _get_module(self, activator:str) -> str:
        for module, configs in self.config.items():
            if activator in configs['activators']:
                return module, configs['default']

        raise ActionNotFoundException(activator=activator)

    def process(self, text:str) -> Generator:
        activator, params = self._parse_user_input(text=text)
        try:
            module, default_messages = self._get_module(activator=activator)
        except ActionNotFoundException as e:
            yield {'result': random.choice(Process.APOLOGY_MESSAGES)}
            return

        if not params and default_messages:
            text = yield {'alert': random.choice(default_messages)}
            params = self._parse_user_input(text, only_params=True)

        module_process = self._get_process_method(module=module)

        yield {'result': module_process(params=params, config=self.config)}


if __name__ == '__main__':
    process = Process()
    # _process = Process.process(
    #     text='control add pin nine with value one hundred in mode pwm'
    # )
    _process = process.process(text='glados')
    p = next(_process)
    if 'alert' in p:
        p = _process.send('glados')
    print(p)
