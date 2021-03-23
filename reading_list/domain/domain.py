from typing import TypedDict


class ReadingEntry:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link


class ReadingEntryStruct(TypedDict):
    title: str
    link: str


class ReadingEntryFactory:

    @staticmethod
    def make_new_entry(title: str, link: str = ""):
        """Examples
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
    def entry_to_struct(entry: ReadingEntry) -> ReadingEntryStruct:
        """Examples:
            >>> reading_entry = ReadingEntry('foo', 'bar')
            >>> ReadingEntryFactory.entry_to_struct(reading_entry)
            {'title': 'foo', 'link': 'bar'}
        """
        return {'title': entry.title, 'link': entry.link}

    @classmethod
    def struct_to_entry(cls, entry_struct: ReadingEntryStruct) -> ReadingEntry:
        """Examples:
            >>> reading_entry_struct = {'title': 'foo', 'link': 'bar'}
            >>> result = ReadingEntryFactory.struct_to_entry(reading_entry_struct)
            >>> f't: {result.title}, l: {result.link}'
            't: foo, l: bar'
        """
        return cls.make_new_entry(entry_struct['title'], entry_struct['link'])
