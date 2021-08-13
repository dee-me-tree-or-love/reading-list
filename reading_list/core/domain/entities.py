from dataclasses import dataclass
from typing import TypedDict


@dataclass
class ReadingEntry:
    title: str
    link: str


class ReadingEntryStruct(TypedDict):
    title: str
    link: str


class ReadingEntryFactory:

    @staticmethod
    def make_new_entry(title: str, link: str = "") -> ReadingEntry:
        """Examples:

            Entry with title and link
            >>> result = ReadingEntryFactory.make_new_entry('foo', 'bar')
            >>> f't: {result.title}, l: {result.link}'
            't: foo, l: bar'

            Entry without link
            >>> result = ReadingEntryFactory.make_new_entry('foo')
            >>> f't: {result.title}, l: {result.link}'
            't: foo, l: '

            Entry without title fails
            >>> result = ReadingEntryFactory.make_new_entry()
            Traceback (most recent call last):
              ...
            TypeError: ...

        """
        return ReadingEntry(title, link)

    @staticmethod
    def entity_to_struct(entry: ReadingEntry) -> ReadingEntryStruct:
        """Examples:

            >>> reading_entry = ReadingEntry('foo', 'bar')
            >>> ReadingEntryFactory.entity_to_struct(reading_entry)
            {'title': 'foo', 'link': 'bar'}
        """
        return {'title': entry.title, 'link': entry.link}

    @classmethod
    def struct_to_entity(cls, entry_struct: ReadingEntryStruct) -> ReadingEntry:
        """Examples:

            >>> reading_entry_struct = {'title': 'foo', 'link': 'bar'}
            >>> result = ReadingEntryFactory.struct_to_entity(reading_entry_struct)
            >>> f't: {result.title}, l: {result.link}'
            't: foo, l: bar'
        """
        return cls.make_new_entry(entry_struct['title'], entry_struct['link'])
