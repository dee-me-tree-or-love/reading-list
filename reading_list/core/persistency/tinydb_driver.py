from reading_list.core.dependencies.keys import DependencyInjectionEntryKeys
from typing import List, cast
from tinydb import TinyDB
from tinydb.table import Document

from reading_list.core.domain.entities import ReadingEntryStruct
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.shared.config import Config, DEFAULT_CONFIGS


class TinyDbDriver:
    DEFAULT_DB_FILE = DEFAULT_CONFIGS.db.tiny_db.location

    def __init__(self, di: ADependencyInjectionContainer):
        self._di = di
        try:
            configs: Config = cast(
                Config, self._di.get(DependencyInjectionEntryKeys.APP_CONFIGS))
            self._db = TinyDB(configs.db.tiny_db.location)
        except Exception:
            self._db = TinyDB(self.DEFAULT_DB_FILE)

    def save(self, reading_entry_struct: ReadingEntryStruct) -> bool:
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
            return self._throwing_save(reading_entry_struct)
        except ValueError:
            return False

    def _throwing_save(self, reading_entry_struct: ReadingEntryStruct) -> bool:
        """Examples:
            >>> from unittest.mock import MagicMock, PropertyMock, patch
            >>> di = dict()
            >>> test_input_entry_struct = dict(title='foo', link='bar')
            >>> def setup_mock_db(mock_db):
            ...     mock_db_instance = MagicMock()
            ...     mock_db.return_value = mock_db_instance
            ...     return mock_db_instance

            1. TinyDbDriver::_throwing_save saves the struct of the reading entry as new Document with custom id
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch.object(TinyDbDriver, '_get_document_id') as mock_get_document_id:
            ...         with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...             mock_db_instance = setup_mock_db(mock_db)
            ...             expected_document = 'some_document'
            ...             expected_document_id = 'some_document_id'
            ...             mock_get_document_id.return_value = expected_document_id
            ...             driver = TinyDbDriver(di)
            ...             _ = driver._throwing_save(test_input_entry_struct)
            ...             mock_document.assert_called_once_with(test_input_entry_struct, expected_document_id)

            2. TinyDbDriver::_throwing_save saves the struct of the reading entry
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch.object(TinyDbDriver, '_get_document_id') as mock_get_document_id:
            ...         with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...             mock_db_instance = setup_mock_db(mock_db)
            ...             mock_document.return_value = expected_document
            ...             driver = TinyDbDriver(di)
            ...             _ = driver._throwing_save(test_input_entry_struct)
            ...             mock_db_instance.insert.assert_called_once_with(expected_document)

            3. TinyDbDriver::_throwing_save returns True if the result of insert is a valid document id
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch.object(TinyDbDriver, '_get_document_id') as mock_get_document_id:
            ...         with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...             mock_db_instance = setup_mock_db(mock_db)
            ...             mock_db_instance.insert.return_value = "some_valid_document_id"
            ...             driver = TinyDbDriver(di)
            ...             driver._throwing_save(test_input_entry_struct)
            True

            4. TinyDbDriver::_throwing_save returns False if the result of insert is not a valid document id
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     with patch.object(TinyDbDriver, '_get_document_id') as mock_get_document_id:
            ...         with patch('reading_list.core.persistency.tinydb_driver.Document') as mock_document:
            ...             mock_db_instance = setup_mock_db(mock_db)
            ...             mock_db_instance.insert.return_value = None
            ...             driver = TinyDbDriver(di)
            ...             driver._throwing_save(test_input_entry_struct)
            False
        """
        new_doc_id = self._get_document_id(reading_entry_struct)
        document_to_store = Document(reading_entry_struct, new_doc_id)
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

    def list(self) -> List[ReadingEntryStruct]:
        """Examples:
            >>> from unittest.mock import MagicMock, PropertyMock, patch
            >>> di = dict()
            >>> def setup_mock_db(mock_db):
            ...     mock_db_instance = MagicMock()
            ...     mock_db.return_value = mock_db_instance
            ...     return mock_db_instance

            1. TinyDbDriver::list retrieves all structs from the database
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     mock_db_instance = setup_mock_db(mock_db)
            ...     driver = TinyDbDriver(di)
            ...     _ = driver.list()
            ...     mock_db_instance.all.assert_called_once_with()

            2. TinyDbDriver::list returns all structs from the database
            >>> with patch.object(TinyDbDriver, '_db', new_callable=PropertyMock) as mock_db:
            ...     mock_db_instance = setup_mock_db(mock_db)
            ...     expected_entry_structs = ['a', 'b', 'c']
            ...     mock_db_instance.all.return_value = expected_entry_structs
            ...     driver = TinyDbDriver(di)
            ...     driver.list()
            ['a', 'b', 'c']
        """
        reading_entry_structs: List[ReadingEntryStruct] = self._db.all()
        return reading_entry_structs
