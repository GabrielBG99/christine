import os, json, nltk, string, random
from inspect import signature
from fuzzywuzzy import fuzz
from typing import Dict, Any, AnyStr, List, Callable
from nltk.stem import LancasterStemmer

from modules import search, board
from utils import exceptions


CONFIG_PATH = os.path.join(os.getcwd(), 'config')
APOLOGIES = [
    "Sorry, I don't know how to do it yet",
    "Sorry, I don't understand" 
]


def get_config() -> Dict[AnyStr, Any]:
    path = os.path.join(CONFIG_PATH, 'commands.json')
    
    with open(path, 'rb') as f:
        config = json.load(f)
    
    return config


def get_feature(feature:str) -> Callable:
    modules = {
        'search': search.search,
        'board': board.control,
    }
    
    if feature not in modules:
        raise ModuleNotFoundError

    return modules[feature]


def _parse_user_input(text:str) -> List[str]:
    stemmer = LancasterStemmer()
    tokens = [
        word for word in nltk.word_tokenize(text.lower()) \
            if word not in string.punctuation
    ]

    return stemmer.stem(tokens[0]), tokens[1:]


def _get_module(activator:str) -> str:
    for module, activators in get_config().items():
        if activator in activators:
            return module

    raise exceptions.ActionNotFound(activator=activator)


def process(text:str):
    activator, params = _parse_user_input(text=text)
    module = _get_module(activator=activator)
    feature = get_feature(feature=module)
    return feature(params)


if __name__ == '__main__':
    response = process(
        text='search glados
    )
    print(response)
