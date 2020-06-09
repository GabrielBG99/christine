#!/usr/bin/env python

import inflect, random, re, csv, os, names
from typing import Dict

p = inflect.engine()

PERCENT_VALUES = [
    '{} percent'.format(
        re.sub(r'\-', ' ', p.number_to_words(x))
    ) for x in range(101)
]

PWM_VALUES = [re.sub(r'\-', ' ', p.number_to_words(x)) for x in range(1024)]

PIN_NAMES = [
    'light',
    'fan',
    'air conditioning',
    'music',
]

PIN_NUMBERS = [
    'pin {}'.format(
        re.sub(r'\-', ' ', p.number_to_words(x))
    ) for x in range(1024)
]

CONFIG = {
    'pin': PIN_NUMBERS + PIN_NAMES,
    'value': ['on', 'off'] + PERCENT_VALUES + PWM_VALUES,
    'action': ['delete', 'add', 'set', 'turn'],
}


def __add_action_config(pin: str) -> str:
    config = random.choice(['', 'pwm', 'analog', 'digital'])
    config = f'as {config}' if config else ''
    name = random.choice(
        [names.get_last_name, names.get_full_name, lambda: '']
    )()
    name = f'{random.choice(["with name", "named"])} {name}' if name else ''
    value = ''
    if config:
        if config in ['analog', 'pwm']:
            value_gen = lambda: random.choice(
                CONFIG['value'] + [''] * round((len(CONFIG['value']) / 5))
            )
            while (value := value_gen()) in ['on', 'off']: pass
        else:
            value = random.choice(['on', 'off', ''])

        value = f'with value {value}' if value else ''
    
    phrase = f'add {pin}'
    extra_args = list(set([config, value, name]))
    while extra_args:
        arg = extra_args.pop(random.choice([i for i in range(len(extra_args))]))
        phrase += ' ' + arg
    return phrase


def _get_test() -> str:
    pin = random.choice(CONFIG['pin'])
    if pin in PIN_NAMES:
        action = random.choice(['set', 'turn'])
    else:
        action = random.choice(CONFIG['action'])
        if action == 'add':
            return __add_action_config(pin=pin)
    value = ''
    if action == 'delete':
        phrase = f'{action} {random.choice(["the ", ""])}{pin}'
    elif action == 'turn':
        value = random.choice(['on', 'off'])
        place = random.choice([0, 1])
        phrase = f'{action} ' 
        phrase += f'{value} ' if place == 0 else ''
        phrase += f'{random.choice(["the ", ""])}{pin}'
        phrase += f' {value}' if place == 1 else ''
    else:
        value = random.choice(CONFIG['value'])
        phrase = f'{action} {random.choice(["the ", ""])}{pin} to {value}'

    return phrase


def generate_responses(test_size: int=20000) -> None:
    test = []
    with open('board_commands.txt', 'w') as f:
        for _ in range(test_size):
            _test = _get_test()
            while list(filter(lambda t: t == _test, test)):
                _test = _get_test()
            test.append(_test + '\n')
        f.writelines(test)


if __name__ == "__main__":
    generate_responses()
