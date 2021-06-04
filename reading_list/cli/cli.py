# TODO:
# 1. build click command runtime for adding new reading list entries
# 2. refactor dependency injection bootstrapping
# 3. implement the click command runtime for listing list entries

from reading_list.core.persistency.tinydb_driver import TinyDbDriver
from reading_list.core.domain.entities import ReadingEntryFactory
from reading_list.core.dependencies.bootstrapper import NaiveBootstrapper
