from reading_list.application.results import AResult, SuccessResult, ErrorResult
from reading_list.domain.entities import ReadingEntry


class BaseHandler:

    def _own_handle(self, event) -> AResult:
        raise NotImplementedError()

    def handle(self, event) -> AResult:
        """Examples:
            >>> from unittest.mock import MagicMock, patch
            
            1. Successful execution of specific handling returns its result
            >>> with patch.object(BaseHandler, '_own_handle') as mock_own_handle:
            ...     expected_result = SuccessResult()
            ...     mock_own_handle.return_value = expected_result
            ...     result = (BaseHandler()).handle("some_event")
            ...     result == expected_result
            True

            2. Error result on an exception
            >>> with patch.object(BaseHandler, '_own_handle') as mock_own_handle:
            ...     mock_own_handle.side_effect = Exception()
            ...     result = (BaseHandler()).handle("some_event")
            ...     isinstance(result, ErrorResult)
            True
        """

        try:
            return self._own_handle(event)
        except:
            return ErrorResult()


class AddEntryCommandHandler(BaseHandler):

    def __init__(self, di_container):
        self._di = di_container

    def _own_handle(self, event) -> AResult:
        return ErrorResult()
        # TODO: implement a solution, for example
        # reading_entry = self._di.get('factory').struct_to_entry(event.data)
        # self._di.get('persistence').save(reading_entry)
        # return SuccessResult()
