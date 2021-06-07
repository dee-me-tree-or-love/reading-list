class ResultStatuses:
    BASE = 'base'
    SUCCESS = 'success'
    ERROR = 'error'

class AResult:
    """Examples:
        >>> result = AResult()
        >>> result.is_ok()
        False
    """
    STATUS = ResultStatuses.BASE

    @classmethod
    def is_ok(cls):
        return cls.STATUS == ResultStatuses.SUCCESS


class SuccessResult(AResult):
    """Examples:
        >>> result = SuccessResult()
        >>> result.is_ok()
        True
    """
    STATUS = ResultStatuses.SUCCESS

class ErrorResult(AResult):
    """Examples:
        >>> result = ErrorResult()
        >>> result.is_ok()
        False
    """
    STATUS = ResultStatuses.ERROR
