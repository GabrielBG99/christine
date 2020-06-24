from attr import attrs, attrib


@attrs
class RequestError(Exception):
    http_status = attrib()
    
    def __str__(self):
        return f'The server returned a {self.http_status} code'

@attrs
class NoResposeFoundException(Exception):
    keyword = attrib()

    def __str__(self):
        return f'Nothing found for "{self.keyword}"'
