from typing import Optional, Dict


class DataInput:
    """Examples:
    >>> d = DataInput()
    >>> d.data = {'foo':'bar'}
    >>> d.data
    {'foo': 'bar'}
    """

    def __init__(self, data: Optional[Dict] = None):
        self._data = data

    @property
    def data(self) -> Dict:
        return self._data or {}

    @data.setter
    def data(self, value: Dict):
        self._data = value
