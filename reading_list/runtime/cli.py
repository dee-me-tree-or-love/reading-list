# TODO:
# 1. build click command runtime for adding new reading list entries
# 2. refactor dependency injection bootstrapping
# 3. implement the click command runtime for listing list entries

from reading_list.persistency.tinydb_driver import TinyDbDriver
from reading_list.domain.entities import ReadingEntryFactory
from reading_list.misc.dependency_injection import ADependencyInjectionContainer, NaiveDependencyInjectionContainer


# TODO: wrap it into a class
def bootstrap_di() -> ADependencyInjectionContainer:
    di = NaiveDependencyInjectionContainer()
    di.register('reading_entry_factory', ReadingEntryFactory)
    di.register('persistence_driver', TinyDbDriver(di))
    return di
