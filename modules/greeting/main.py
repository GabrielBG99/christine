import random
from typing import Dict, Any


def process(**kwargs) -> Dict[str, Any]:
    config = kwargs['config']['greeting']
    return {'speak': random.choice(config['default'])}


if __name__ == "__main__":
    import os, json
    path = os.path.join(
        os.getcwd(), 
        'config', 
        'commands.json'
    )
    with open(path, 'rb') as f:
        config = json.load(f)
    process(config=config)
