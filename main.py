#!/usr/bin/python

from engine import Bot


if __name__ == "__main__":
    engine = Bot()

    while True:
        command = engine.request_command()
        result = engine.process(text=command)
        if 'speak' in result: engine.say(phrase=result['speak'])
        print(result)
