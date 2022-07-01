from argon2 import PasswordHasher
from src.shared.exceptions.businessException import BusinessException

class PasswordHelper:
    @staticmethod
    def hash(password):
        ph = PasswordHasher()
        return ph.hash(password)

    @staticmethod
    def checkPassword(storedPassword, inputPassword, errorCode):
        try:
            ph = PasswordHasher()
            res = ph.verify(storedPassword, inputPassword)
            if not res:
                raise BusinessException(errorCode)
        except Exception as e:
            raise BusinessException(errorCode)