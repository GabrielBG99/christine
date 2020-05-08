#!/usr/bin/env python
import inflect, random, re, csv, os

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
    'action': ['delete', 'change', 'add', 'set', 'turn'],
}


def _get_test():
    pin = random.choice(CONFIG['pin'])
    if pin in PIN_NAMES:
        action = random.choice(['change', 'set', 'turn'])
    else:
        action = random.choice(CONFIG['action'])
    value = ''
    if action in ['delete', 'add']:
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

    return {
        'phrase': phrase,
        'pin': pin.replace('pin ', ''),
        'value': value,
        'action': action
    }


def generate_responses():
    test = []
    with open('board_commands.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['phrase','pin','value','action'])
        writer.writeheader()
        for _ in range(20000):
            _test = _get_test()
            while list(filter(lambda t: t['phrase'] == _test['phrase'], test)):
                _test = _get_test()
            test.append(_test)
            writer.writerow(_test)


if __name__ == "__main__":
    generate_responses()
