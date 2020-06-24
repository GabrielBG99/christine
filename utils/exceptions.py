from attr import attrs, attrib


@attrs
class ActionNotFoundException(Exception):
    activator = attrib(type=str)

    def __str__(self):
        return f'The action for "{self.activator}" was not found'

@attrs
class ModuleNotConfiguredException(Exception):
    name = attrib(type=str)

    def __str__(self):
        return f'No module named "{self.name}" was found'

@attrs
class InvalidCommandException(Exception):
    command = attrib(type=str)

    def __str__(self):
        return f'No command named "{self.command}" was found'
