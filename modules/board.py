from typing import List, Dict, Any
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from utils.w2n import Word2Number
from utils.exceptions import InvalidCommand


VALID_COMMANDS = ['delete', 'add', 'set', 'turn']


def _get_value(words: List[str], target: str) -> str:
    try:
        return words[words.index(target) + 1]
    except ValueError:
        return ''


def _get_pin(phrase: str, command: str) -> Dict[str, Any]:
    words = phrase.split()
    pin = words[words.index('pin') + 1]
    return {
        'command': command,
        'pin': pin,
    }


def _action_add(phrase: str) -> Dict[str, Any]:
    words = phrase.split()
    name = None
    porter = PorterStemmer()
    for i, word in enumerate(words[:]):
        if porter.stem(word) == 'name':
            name = words[i + 1]
            break
    action = _get_pin(command='add', phrase=phrase)
    action.update({
        'name': name,
        'value': _get_value(words=words, target='value') or None,
        'config': _get_value(words=words, target='as') or None,
    })
    return action


def _action_set(phrase: str) -> Dict[str, Any]:
    words = phrase.split()
    if 'pin' in words:
        pin = words[words.index('pin') + 1]
    else:
        porter = PorterStemmer()
        _words = [
            word for word in words \
                if (
                    word != 'set' and
                    not Word2Number.is_number(word) and
                    porter.stem(word) not in stopwords.words('english')
                )
        ]
        pin = ' '.join(_words)
    return {
        'command': 'set',
        'pin': pin,
        'value': _get_value(words=words, target='to'),
    }


def _action_turn(phrase: str) -> Dict[str, Any]:
    words = phrase.split()
    if 'pin' in words:
        pin = words[words.index('pin') + 1]
    else:
        porter = PorterStemmer()
        _words = [
            word for word in words \
                if (
                    word != 'turn' and
                    porter.stem(word) not in stopwords.words('english')
                )
        ]
        pin = ' '.join(_words)
    
    return {
        'command': 'turn',
        'pin': pin,
        'value': True if 'on' in words else False
    }


def process_input(text: str) -> Dict[str, Any]:
    w2n = Word2Number()
    text_parsed = w2n.parse(text)
    command = text_parsed.split()[0]
    
    if command not in VALID_COMMANDS:
        raise InvalidCommand(command=command) 

    return {
        'add': lambda: _action_add(phrase=text_parsed),
        'delete': lambda: _get_pin(command='delete', phrase=text_parsed),
        'set': lambda: _action_set(phrase=text_parsed),
        'turn': lambda: _action_turn(phrase=text_parsed),
    }[command]()
