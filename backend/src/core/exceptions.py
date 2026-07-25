
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

#------------------------------------------------------------------------------------------------------------


class MediaDomainException(Exception):
    """Base exception for media domain errors."""
    pass

class InvalidFileTypeException(MediaDomainException):
    """Raised when the requested MIME type is not allowed."""
    pass

class FileTooLargeException(MediaDomainException):
    """Raised when requested file size exceeds max allowed bytes."""
    pass


class ImageNotFoundException(MediaDomainException):
    """Raised when no pending upload record is found matching the key/ID."""
    pass

class UploadConfirmationFailedException(MediaDomainException):
    """Raised when S3 head_object fails or object is missing in S3."""
    pass

class CorruptedUploadException(MediaDomainException):
    """Raised when actual uploaded file size/type in S3 mismatches requested metadata."""
    pass

class ImageNotFoundException(MediaDomainException):
    """Raised when an image ID does not exist in the database."""
    pass

class ImageExpiredException(MediaDomainException):
    """Raised when trying to access an image past its 24-hour expiration date."""
    pass

class ImageAlreadyViewedException(MediaDomainException):
    """Raised when a user attempts to view a view-once image again."""
    pass

class ImageUnauthorizedAccessException(MediaDomainException):
    """Raised when a non-friend tries to access a private media resource."""
    pass

class MediaDatabaseException(MediaDomainException):
    """Raised when a database transaction or commit fails."""
    pass

#------------------------------------------------------------------------------------------------------------



class FriendsFeedException(MediaDomainException):
    """Base exception for friend feed operations."""
    pass

class NoFriendsFoundException(FriendsFeedException):
    """Raised when user attempts to load a feed but has no friends yet."""
    pass

class EmptyFeedException(FriendsFeedException):
    """Raised when there are no unviewed or active images in the feed."""
    pass