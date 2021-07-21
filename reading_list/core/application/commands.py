from reading_list.core.application.inputs import DataInputEvent
from reading_list.core.application.results import AResult, SuccessResult, ErrorResult
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.core.dependencies.bootstrapper import DependencyInjectionEntryKeys


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
            >>> di = dict(reading_entry_factory=mock_factory, persistence_driver=mock_persistence)
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
        reading_factory = self._di.get(
            DependencyInjectionEntryKeys.READING_ENTRY_FACTORY)
        persistency_driver = self._di.get(
            DependencyInjectionEntryKeys.PERSISTENCE_DRIVER)
        reading_entry = reading_factory.struct_to_entity(event.data)
        result = persistency_driver.save(reading_entry)
        return SuccessResult() if result else ErrorResult()

class ListEntriesCommandHandler(BaseHandler):
    def _own_handle(self, _: DataInputEvent) -> AResult:
        """Examples:
            >>> from unittest.mock import MagicMock, patch
            >>> mock_persistence = MagicMock()
            >>> di = dict(persistence_driver=mock_persistence)
            >>> mock_event = None
            >>> command_handler = ListEntriesCommandHandler(di)
            >>> def reset_mocks():
            ...     mock_persistence.reset_mock()

            1. ListEntriesCommandHandler::_own_handle retrieves a list of entries from the persistency driver
            >>> reset_mocks()
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_persistence.list.assert_called_once_with()

            2. ListEntriesCommandHandler::_own_handle returns a list of entries as data of the result
            >>> reset_mocks()
            >>> expected_reading_items = ['Vango', 'We', '451']
            >>> mock_persistence.list.return_value = expected_reading_items
            >>> result = command_handler._own_handle(mock_event)
            >>> result.data['entries'] == expected_reading_items
            True
        """
        persistency_driver = self._di.get(
            DependencyInjectionEntryKeys.PERSISTENCE_DRIVER)
        reading_entries = persistency_driver.list()
        return SuccessResult(data={'entries': reading_entries})