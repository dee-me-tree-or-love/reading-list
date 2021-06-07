from tinydb import TinyDB
from tinydb.table import Document

from reading_list.core.domain.entities import ReadingEntry, ReadingEntryStruct
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer


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

            >>> from unittest.mock import MagicMock, PropertyMock, patch
            >>> mock_factory = MagicMock()
            >>> di = dict(reading_entry_factory=mock_factory)
            >>> test_input_entry = MagicMock()
            >>> test_input_entry.title = "some_title"
            >>> test_input_entry.link = "some_link"
            >>> def get_test_entry_struct(reading_entry):
            ...     return dict(title=reading_entry.title, link=reading_entry.link)
            >>> def setup_mock_db(mock_db):
            ...     mock_db_instance = MagicMock()
            ...     mock_db.return_value = mock_db_instance
            ...     return mock_db_instance
            >>> def setup_mock_factory():
            ...     expected_struct = get_test_entry_struct(test_input_entry)
            ...     mock_factory.entity_to_struct.return_value = expected_struct
            >>> def reset_mocks():
            ...     mock_factory.reset_mock()

            1. TinyDbDriver::_throwing_save uses the struct of the reading entry
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...         reset_mocks()
            ...         setup_mock_factory()
            ...         driver = TinyDbDriver(di)
            ...         _ = driver._throwing_save(test_input_entry)
            ...         mock_factory.entity_to_struct.assert_called_once_with(test_input_entry)

            2. TinyDbDriver::_throwing_save saves the struct of the reading entry
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...         reset_mocks()
            ...         setup_mock_factory()
            ...         mock_db_instance = setup_mock_db(mock_db)
            ...         expected_document = "some_document"
            ...         mock_document.return_value = expected_document
            ...         driver = TinyDbDriver(di)
            ...         _ = driver._throwing_save(test_input_entry)
            ...         mock_db_instance.insert.assert_called_once_with(expected_document)

            3. TinyDbDriver::_throwing_save returns True if the result of insert is a valid document id
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...         reset_mocks()
            ...         setup_mock_factory()
            ...         mock_db_instance = setup_mock_db(mock_db)
            ...         mock_db_instance.insert.return_value = "some_valid_document_id"
            ...         driver = TinyDbDriver(di)
            ...         driver._throwing_save(test_input_entry)
            True

            4. TinyDbDriver::_throwing_save returns False if the result of insert is not a valid document id
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...         reset_mocks()
            ...         setup_mock_factory()
            ...         mock_db_instance = setup_mock_db(mock_db)
            ...         mock_db_instance.insert.return_value = None
            ...         driver = TinyDbDriver(di)
            ...         driver._throwing_save(test_input_entry)
            False
        """
        factory = self._di.get('reading_entry_factory')
        reading_entry_struct: ReadingEntryStruct = factory.entity_to_struct(
            reading_entry)
        document_to_store = Document(
            reading_entry_struct, doc_id=self._get_document_id(reading_entry_struct))
        entry_id = self._db.insert(document_to_store)
        return True if entry_id else False

    def _get_document_id(self, reading_entry_struct: ReadingEntryStruct) -> int:
        """Examples:

            >>> from unittest.mock import MagicMock, patch
            >>> mock_factory = MagicMock()
            >>> di = dict(reading_entry_factory=mock_factory)
            >>> test_instance = TinyDbDriver(di)

            1. Returns same integer for same reading_entry_struct titles
            >>> entry_a = dict(title="carl")
            >>> entry_b = dict(title="carl")
            >>> id_a = test_instance._get_document_id(entry_a)
            >>> id_b = test_instance._get_document_id(entry_b)
            >>> id_a == id_b
            True

            2. Returns same integer for reading_entry_struct titles ingoring capital cases
            >>> entry_a = dict(title="carl")
            >>> entry_b = dict(title="CaRl")
            >>> id_a = test_instance._get_document_id(entry_a)
            >>> id_b = test_instance._get_document_id(entry_b)
            >>> id_a == id_b
            True

            3. Returns different integers for reading_entry_struct with different titles
            >>> entry_a = dict(title="carl")
            >>> entry_b = dict(title="CaRlos Iv")
            >>> id_a = test_instance._get_document_id(entry_a)
            >>> id_b = test_instance._get_document_id(entry_b)
            >>> id_a == id_b
            False
        """
        lower_title = reading_entry_struct['title'].lower()
        return int.from_bytes(lower_title.encode(), byteorder='big')
