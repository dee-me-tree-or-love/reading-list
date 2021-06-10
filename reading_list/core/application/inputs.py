from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class DataInputEvent:
    data: Dict[str, Any] = field(default_factory=dict)

class InputEventFactory:
    @staticmethod
    def make_data_input_event(data_body: Dict[str, Any]) -> DataInputEvent:
        """Examples:
            1. Creates a DataInputEvent with provided body
            >>> result = InputEventFactory.make_data_input_event({'foo':'bar'})
            >>> isinstance(result, DataInputEvent)
            True
            >>> result.data
            {'foo': 'bar'}
        """
        return DataInputEvent(data=data_body)