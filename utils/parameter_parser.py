from typing import Any
from word2number.w2n import word_to_num


def parse_param(param:str) -> Any:
    try:
        return word_to_num(param)
    except Exception:
        try:
            return {
                'on': True,
                'off': False
            }[param]
        except KeyError:
            return param
