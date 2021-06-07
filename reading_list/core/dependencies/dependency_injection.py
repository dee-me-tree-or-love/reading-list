from typing import Any, Dict
from abc import ABC, abstractmethod


class ADependencyInjectionContainer(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._container: Dict[str, Any] = {}

    @abstractmethod
    def register(self, key: str, item: Any) -> bool:
        ...

    @abstractmethod
    def get(self, key: str) -> Any:
        ...


class NaiveDependencyInjectionContainer(ADependencyInjectionContainer):
    """Examples:

        1. Starts with an empty container
        >>> di = NaiveDependencyInjectionContainer()
        >>> di._container
        {}
    """

    def register(self, key: str, item: Any) -> bool:
        """Examples:

            1. Adding a new item with key to an empty container returns True
            >>> some_item = 4
            >>> some_key = 'hidden_number'
            >>> di = NaiveDependencyInjectionContainer()
            >>> di.register(some_key, some_item)
            True

            1.1. The added item is stored in the container
            >>> some_item = 4
            >>> some_key = 'hidden_number'
            >>> di = NaiveDependencyInjectionContainer()
            >>> _ = di.register(some_key, some_item)
            >>> di._container
            {'hidden_number': 4}

        """
        self._container[key] = item
        return True

    def get(self, key: str) -> Any:
        """Examples:

            1. Gets an item from the container known with this key
            >>> di = NaiveDependencyInjectionContainer()
            >>> di._container = {'some_key': 'the ring'}
            >>> di.get('some_key')
            'the ring'

            2. Raise a value error if the key is not known
            >>> di = NaiveDependencyInjectionContainer()
            >>> di._container = {'some_key': 'the ring'}
            >>> di.get('some_unknown_key')
            Traceback (most recent call last):
                ...
            ValueError: ...
        """
        try:
            return self._container[key]
        except KeyError as error:
            raise ValueError(f'Provided key "{key}" is unknown.') from error
