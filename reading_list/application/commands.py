from reading_list.application.inputs import DataInputEvent
from reading_list.application.results import AResult, SuccessResult, ErrorResult
from reading_list.misc.dependency_injection import ADependencyInjectionContainer


class BaseHandler:
    def __init__(self, di_container: ADependencyInjectionContainer):
        self._di = di_container

    def _own_handle(self, event: DataInputEvent) -> AResult:
        raise NotImplementedError()

    def handle(self, event: DataInputEvent) -> AResult:
        """Examples:
            >>> from unittest.mock import MagicMock, patch
            >>> def get_base_handler():
            ...     di = dict()
            ...     return BaseHandler(di)

            1. Successful execution of specific handling returns its result
            >>> with patch.object(BaseHandler, '_own_handle') as mock_own_handle:
            ...     expected_result = SuccessResult()
            ...     mock_own_handle.return_value = expected_result
            ...     result = (get_base_handler()).handle("some_event")
            ...     result == expected_result
            True

            2. Error result on an exception
            >>> with patch.object(BaseHandler, '_own_handle') as mock_own_handle:
            ...     mock_own_handle.side_effect = Exception()
            ...     result = (get_base_handler()).handle("some_event")
            ...     isinstance(result, ErrorResult)
            True
        """
        try:
            return self._own_handle(event)
        except:
            return ErrorResult()


class AddEntryCommandHandler(BaseHandler):
    def _own_handle(self, event: DataInputEvent) -> AResult:
        """Examples:
            >>> from unittest.mock import MagicMock, patch
            >>> mock_factory = MagicMock()
            >>> mock_persistence = MagicMock()
            >>> di = dict(reading_entry_factory=mock_factory, persistence=mock_persistence)
            >>> command_handler = AddEntryCommandHandler(di)
            >>> mock_event = MagicMock
            >>> mock_event.data = "some_data"
            >>> def reset_mocks():
            ...     mock_factory.reset_mock()
            ...     mock_persistence.reset_mock()

            1. AddEntryCommandHandler::_own_handle converts the event data to an entity
            >>> reset_mocks()
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_factory.struct_to_entity.assert_called_once_with(mock_event.data)

            2. AddEntryCommandHandler::_own_handle saves the entity
            >>> reset_mocks()
            >>> expected_entity = "amazing reading entry"
            >>> mock_factory.struct_to_entity.return_value = expected_entity
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_persistence.save.assert_called_once_with(expected_entity)

            3. AddEntryCommandHandler::_own_handle returns SuccessResult if saving succeeds
            >>> reset_mocks()
            >>> expected_entity = "amazing reading entry"
            >>> mock_factory.struct_to_entity.return_value = expected_entity
            >>> mock_persistence.save.return_value = True
            >>> result = command_handler._own_handle(mock_event)
            >>> isinstance(result, SuccessResult)
            True

            4. AddEntryCommandHandler::_own_handle returns ErrorResult if saving fails
            >>> reset_mocks()
            >>> expected_entity = "amazing reading entry"
            >>> mock_factory.struct_to_entity.return_value = expected_entity
            >>> mock_persistence.save.return_value = False
            >>> result = command_handler._own_handle(mock_event)
            >>> isinstance(result, ErrorResult)
            True
        """
        reading_factory = self._di.get('reading_entry_factory')
        reading_entry = reading_factory.struct_to_entity(event.data)
        result = self._di.get('persistence').save(reading_entry)
        return SuccessResult() if result else ErrorResult()
