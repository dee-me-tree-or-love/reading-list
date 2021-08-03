from typing import List
from reading_list.core.domain.entities import ReadingEntry, ReadingEntryStruct
from reading_list.core.application.inputs import DataInputEvent
from reading_list.core.application.results import AResult, SuccessResult, ErrorResult
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.core.dependencies.keys import DependencyInjectionEntryKeys


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

            1. AddEntryCommandHandler::_own_handle cleans the incoming data into a reading entry struct
            >>> reset_mocks()
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_factory.struct_to_entity.assert_called_once_with(mock_event.data)
            >>> mock_factory.entity_to_struct.assert_called_once_with(mock_factory.struct_to_entity.return_value)

            2. AddEntryCommandHandler::_own_handle saves the clean struct
            >>> reset_mocks()
            >>> expected_struct = "amazing reading entry struct"
            >>> mock_factory.entity_to_struct.return_value = expected_struct
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_persistence.save.assert_called_once_with(expected_struct)

            3. AddEntryCommandHandler::_own_handle returns SuccessResult if saving succeeds
            >>> reset_mocks()
            >>> mock_persistence.save.return_value = True
            >>> result = command_handler._own_handle(mock_event)
            >>> isinstance(result, SuccessResult)
            True

            4. AddEntryCommandHandler::_own_handle returns ErrorResult if saving fails
            >>> reset_mocks()
            >>> mock_persistence.save.return_value = False
            >>> result = command_handler._own_handle(mock_event)
            >>> isinstance(result, ErrorResult)
            True
        """
        factory = self._di.get(
            DependencyInjectionEntryKeys.READING_ENTRY_FACTORY)
        persistency = self._di.get(
            DependencyInjectionEntryKeys.PERSISTENCE_DRIVER)
        reading_entry = factory.struct_to_entity(event.data)
        clean_reading_entry_struct = factory.entity_to_struct(
            reading_entry)
        # TODO: add check for possible input errors: already exists / invalid data etc...
        result = persistency.save(clean_reading_entry_struct)
        return SuccessResult() if result else ErrorResult()


class ListEntriesCommandHandler(BaseHandler):
    def _own_handle(self, _: DataInputEvent) -> AResult:
        """Examples:
            >>> from unittest.mock import MagicMock, patch
            >>> mock_factory = MagicMock()
            >>> mock_persistence = MagicMock()
            >>> di = dict(reading_entry_factory=mock_factory, persistence_driver=mock_persistence)
            >>> mock_event = None
            >>> command_handler = ListEntriesCommandHandler(di)
            >>> def reset_mocks():
            ...     mock_factory.reset_mock()
            ...     mock_persistence.reset_mock()

            1. ListEntriesCommandHandler::_own_handle retrieves a list of structs from the persistency driver
            >>> reset_mocks()
            >>> _ = command_handler._own_handle(mock_event)
            >>> mock_persistence.list.assert_called_once_with()

            2. ListEntriesCommandHandler::_own_handle returns a list of entries as data of the result
            >>> reset_mocks()
            >>> expected_reading_entry_structs = ['a', 'b', 'c']
            >>> mock_persistence.list.return_value = expected_reading_entry_structs
            >>> mock_factory.struct_to_entity.side_effect = lambda x: f'<entity>_{x}'
            >>> result = command_handler._own_handle(mock_event)
            >>> result.data['entries']
            ['<entity>_a', '<entity>_b', '<entity>_c']
        """
        factory = self._di.get(
            DependencyInjectionEntryKeys.READING_ENTRY_FACTORY)
        persistency = self._di.get(
            DependencyInjectionEntryKeys.PERSISTENCE_DRIVER)
        reading_entry_structs: List[ReadingEntryStruct] = persistency.list()
        reading_entries: List[ReadingEntry] = list(
            map(factory.struct_to_entity, reading_entry_structs))
        return SuccessResult(data={'entries': reading_entries})
