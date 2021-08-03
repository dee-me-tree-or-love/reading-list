
from abc import ABC, abstractmethod
from typing import Any, Type

from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer
from reading_list.core.dependencies.keys import DependencyInjectionEntryKeys
from reading_list.core.domain.entities import ReadingEntryFactory
from reading_list.core.persistency.tinydb_driver import TinyDbDriver
from reading_list.shared.config import AConfig


class BootstrapperValueFactories:
    @staticmethod
    def READING_ENTRY_FACTORY(_: Any) -> Type[ReadingEntryFactory]:
        return ReadingEntryFactory

    @staticmethod
    def PERSISTENCE_DRIVER(container: ADependencyInjectionContainer) -> TinyDbDriver:
        return TinyDbDriver(container)


class ADependencyInjectionBootstrapper(ABC):

    @abstractmethod
    def bootstrap_with_configurations(self, configs: AConfig) -> ADependencyInjectionContainer:
        ...


class NaiveDependencyInjectionBootstrapper(ADependencyInjectionBootstrapper):
    def __init__(self, container: ADependencyInjectionContainer) -> None:
        """Examples:
            1. New bootstrapper takes in the container
            >>> from unittest.mock import MagicMock
            >>> mock_di_container = MagicMock()
            >>> test_instance = NaiveDependencyInjectionBootstrapper(mock_di_container)
            >>> test_instance._di_container == mock_di_container
            True
        """
        self._di_container = container

    def bootstrap_with_configurations(self, configs: AConfig) -> ADependencyInjectionContainer:
        self._di_container.register(DependencyInjectionEntryKeys.APP_CONFIGS,
                                    configs)
        self._di_container.register(DependencyInjectionEntryKeys.READING_ENTRY_FACTORY,
                                    BootstrapperValueFactories.READING_ENTRY_FACTORY(self))
        self._di_container.register(DependencyInjectionEntryKeys.PERSISTENCE_DRIVER,
                                    BootstrapperValueFactories.PERSISTENCE_DRIVER(self._di_container))
        return self._di_container
