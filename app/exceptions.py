class AutomationBaseException(Exception):
    """Base exception for all automation errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BusinessException(AutomationBaseException):
    """
    Raised when the target UI or data fails a business validation rule
    (e.g., 'Account locked', 'Customer identity could not be verified').
    """
    pass


class ApplicationException(AutomationBaseException):
    """
    Raised when technical or infrastructure failures occur
    (e.g., ElementNotFound, 502 Bad Gateway on target site, Network timeout).
    """
    pass
