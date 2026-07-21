
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

class UserNotLoggedIn(AuthDomainException):
    """Raise when a user uses the service without logged in"""
    pass

class UserNotFound(AuthDomainException):
    """Raise when a user is not Present"""
    pass

#------------------------------------------------------------------------------------------------------------

class FriendDomainException(Exception):
    """Base exception for all Friendship domain errors."""
    pass

class SelfConnectionException(FriendDomainException):
    """Cant Sent Youself the Friendship request"""
    pass

class friendshipAlreadyExistsException(FriendDomainException):
    """Friendship request Already Sent or Denied or Blocked"""
    pass

class friendshipRequestNotExists(FriendDomainException):
    """Friendship request by this users not present"""
    pass