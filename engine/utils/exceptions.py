from dataclasses import dataclass


@dataclass
class ActionNotFoundException(Exception):
    activator: str

    def __str__(self):
        return f'The action for "{self.activator}" was not found'

@dataclass
class ModuleNotConfiguredException(Exception):
    name: str

    def __str__(self):
        return f'No module named "{self.name}" was found'

@dataclass
class InvalidCommandException(Exception):
    command: str

    def __str__(self):
        return f'No command named "{self.command}" was found'
