from src.shared.exceptions.responseMessages import ResponseMessages

class BusinessException(Exception):
    def __init__(self, code, language = None):
        self.code = code
        self.message = ResponseMessages.english[code]
        super().__init__(self.message)