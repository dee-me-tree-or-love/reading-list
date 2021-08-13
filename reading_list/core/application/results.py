from typing import Any, Dict, Optional


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

    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Examples:

            >>> data = {'foo': 'bar'}
            >>> result = AResult(data=data)
            >>> result.data == data
            True
        """
        self.data: Dict[str, Any] = data or {}

    @classmethod
    def is_ok(cls) -> bool:
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
