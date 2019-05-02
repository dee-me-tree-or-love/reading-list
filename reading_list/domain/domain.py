class EntryStatus:
    PENDING = 'pending'
    DOWNLOADED = 'downloaded'
    READ = 'read'


class ReadingEntry:
    DEFAULT_STATUS = EntryStatus.PENDING

    def __init__(self, title, url, status=None):
        self.title = title
        self.url = url
        self.status = self.DEFAULT_STATUS if status == None else status


class ReadingEntryFactory:

    @staticmethod
    def make_new_entry(title=None, url=None):
        if title == None or url == None:
            raise ValueError("title and url must be provided")
        return ReadingEntry(title, url)

    @staticmethod
    def map_to_entry_struct(entry):
        return {
            'title': entry.title,
            'url': entry.url,
            'status': entry.status
        }

    @staticmethod
    def map_struct_to_entry(entry_struct):
        return ReadingEntry(
            entry_struct['title'], entry_struct['url'], entry_struct['status'])
