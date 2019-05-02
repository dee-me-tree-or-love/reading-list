import logging

from tinydb import TinyDB, Query

logger = logging.getLogger(__name__)


class TinyDbDriver:
    DB_FILE = 'db.json'

    def __init__(self):
        self.db = TinyDB(self.DB_FILE)

    def save(self, reading_entry_data):
        logger.critical(reading_entry_data)
        entry_id = self.db.insert(reading_entry_data)
        logger.critical(entry_id)
        return entry_id
