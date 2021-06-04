
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.core.domain.entities import ReadingEntryFactory
from reading_list.core.persistency.tinydb_driver import TinyDbDriver


class DEPENDENCY_INJECTION_ENTRY_KEYS:
    READING_ENTRY_FACTORY = 'reading_entry_factory'
    PERSISTENCE_DRIVER = 'persistence_driver'


class BOOTSTRAPPER_VALUE_LOADERS:
    @staticmethod
    def READING_ENTRY_FACTORY(_) -> ReadingEntryFactory:
        return ReadingEntryFactory

    @staticmethod
    def PERSISTENCE_DRIVER(container: ADependencyInjectionContainer) -> TinyDbDriver:
        return TinyDbDriver(container)


class NaiveBootstrapper:
    def __init__(self, container: ADependencyInjectionContainer) -> None:
        self._container = container

    def bootstrap_di(self) -> ADependencyInjectionContainer:
        self._container.register(DEPENDENCY_INJECTION_ENTRY_KEYS.READING_ENTRY_FACTORY,
                                 BOOTSTRAPPER_VALUE_LOADERS.READING_ENTRY_FACTORY(self))
        self._container.register(DEPENDENCY_INJECTION_ENTRY_KEYS.PERSISTENCE_DRIVER,
                                 BOOTSTRAPPER_VALUE_LOADERS.PERSISTENCE_DRIVER(self._container))
        return self._container
