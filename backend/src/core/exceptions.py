
class AuthDomainException(Exception):
    """Base exception for all authentication domain errors."""
    pass

class UserAlreadyExistsException(AuthDomainException):
    """Raised when a user tries to register with an email already in use."""
    pass

class UserEmailNotExists(AuthDomainException):
    """Raised when a user enters non existing email"""
    pass

class UserPasswordNotMatched(AuthDomainException):
    """Raise when a user enters wrong Password"""
    pass
