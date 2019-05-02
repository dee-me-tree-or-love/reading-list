from reading_list.application.results import SuccessResult, ErrorResult
from reading_list.domain.domain import ReadingEntryFactory


class AddEntryHandler:

    def __init__(self, input_adapter, output_adapter, persistency_driver):
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter
        self.persistency_driver = persistency_driver

        self.reading_entry_factory = ReadingEntryFactory

    def handle(self, event):
        entry_data = self.input_adapter.get_data(event)
        reading_entry = self.reading_entry_factory.make_new_entry(
            title=entry_data['title'], url=entry_data['url'])
        try:
            reading_entry_data = self.reading_entry_factory.map_to_entry_struct(
                reading_entry)
            self.persistency_driver.save(reading_entry_data)
            return self.output_adapter.resolve(SuccessResult())
        except Exception as e:
            return self.output_adapter.resolve(ErrorResult(e))
