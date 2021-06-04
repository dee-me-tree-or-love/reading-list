
from typing import Any, Type
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.core.domain.entities import ReadingEntryFactory
from reading_list.core.persistency.tinydb_driver import TinyDbDriver


class DependencyInjectionEntryKeys:
    READING_ENTRY_FACTORY = 'reading_entry_factory'
    PERSISTENCE_DRIVER = 'persistence_driver'


class BootstrapperValueFactories:
    @staticmethod
    def READING_ENTRY_FACTORY(_: Any) -> Type[ReadingEntryFactory]:
        return ReadingEntryFactory

    @staticmethod
    def PERSISTENCE_DRIVER(container: ADependencyInjectionContainer) -> TinyDbDriver:
        return TinyDbDriver(container)


class NaiveBootstrapper:
    def __init__(self, container: ADependencyInjectionContainer) -> None:
        self._container = container

    def bootstrap_di(self) -> ADependencyInjectionContainer:
        self._container.register(DependencyInjectionEntryKeys.READING_ENTRY_FACTORY,
                                 BootstrapperValueFactories.READING_ENTRY_FACTORY(self))
        self._container.register(DependencyInjectionEntryKeys.PERSISTENCE_DRIVER,
                                 BootstrapperValueFactories.PERSISTENCE_DRIVER(self._container))
        return self._container
