from typing import AnyStr


class RequestError(Exception):
    def __init__(self, http_status:int, description:AnyStr):
        self.http_status = http_status
        self.description = description
    
    def __str__(self):
        return f'The server retouned a {self.http_status} code'


class ActionNotFound(Exception):
    def __init__(self, activator:str):
        self.activator = activator

    def __str__(self):
        return f'The action for "{self.activator}" was not found'
