from tinydb import TinyDB

from reading_list.domain.entities import ReadingEntry
from reading_list.misc.dependency_injection import ADependencyInjectionContainer


class TinyDbDriver:
    DB_FILE = 'db.json'
    _db = TinyDB(DB_FILE)

    def __init__(self, di: ADependencyInjectionContainer):
        self._di = di

    def save(self, reading_entry: ReadingEntry) -> bool:
        """Examples:

            >>> from unittest.mock import MagicMock, patch
            >>> di = dict()
            >>> test_input_entry = MagicMock()

            1. TinyDbDriver::save returns the result of a "throwing" save if all goes well
            >>> with patch.object(TinyDbDriver, '_throwing_save') as mock_throwing_save:
            ...     mock_throwing_save.return_value = True
            ...     driver = TinyDbDriver(di)
            ...     driver.save(test_input_entry)
            True

            2. TinyDbDriver::save returns false if "_throwing_save" raises ValueError
            >>> with patch.object(TinyDbDriver, '_throwing_save') as mock_throwing_save:
            ...     mock_throwing_save.side_effect = ValueError('invalid input')
            ...     driver = TinyDbDriver(di)
            ...     driver.save(test_input_entry)
            False
        """
        try:
            return self._throwing_save(reading_entry)
        except ValueError:
            return False

    def _throwing_save(self, reading_entry: ReadingEntry) -> bool:
        """Examples:

            >>> from unittest.mock import MagicMock, patch
            >>> mock_factory = MagicMock()
            >>> di = dict(reading_entry_factory=mock_factory)
            >>> test_input_entry = MagicMock()
            >>> def reset_mocks():
            ...     mock_factory.reset_mock()

            1. TinyDbDriver::_throwing_save uses the struct of the reading entry
            >>> with patch.object(TinyDbDriver, '_db') as mock_db:
            ...     reset_mocks()
            ...     driver = TinyDbDriver(di)
            ...     _ = driver._throwing_save(test_input_entry)
            ...     mock_factory.entity_to_struct.assert_called_once_with(test_input_entry)

            2. TinyDbDriver::_throwing_save saves the struct of the reading entry
            >>> with patch.object(TinyDbDriver, '_db') as mock_db:
            ...     reset_mocks()
            ...     expected_struct = "some_struct"
            ...     mock_factory.entity_to_struct.return_value = expected_struct
            ...     driver = TinyDbDriver(di)
            ...     _ = driver._throwing_save(test_input_entry)
            ...     mock_db.insert.assert_called_once_with(expected_struct)

            3. TinyDbDriver::_throwing_save returns True if the result of insert is a valid document id
            >>> with patch.object(TinyDbDriver, '_db') as mock_db:
            ...     reset_mocks()
            ...     mock_db.insert.return_value = "some_valid_document_id"
            ...     driver = TinyDbDriver(di)
            ...     driver._throwing_save(test_input_entry)
            True

            4. TinyDbDriver::_throwing_save returns False if the result of insert is not a valid document id
            >>> with patch.object(TinyDbDriver, '_db') as mock_db:
            ...     reset_mocks()
            ...     mock_db.insert.return_value = None
            ...     driver = TinyDbDriver(di)
            ...     driver._throwing_save(test_input_entry)
            False
        """
        factory = self._di.get('reading_entry_factory')
        reading_entry_struct = factory.entity_to_struct(reading_entry)
        entry_id = self._db.insert(reading_entry_struct)
        return True if entry_id else False
