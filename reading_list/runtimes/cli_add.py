from reading_list.application.handlers import AddEntryHandler
from reading_list.persistency.tinydb_driver import TinyDbDriver
from unittest.mock import MagicMock
import click


def create_add_entry_handler():
    input_adapter = MagicMock()
    input_adapter.get_data.side_effect = lambda x: x
    output_adapter = MagicMock()
    output_adapter.resolve.side_effect = lambda x: click.echo(
        "Resolving with %s" % str(x))
    handler = AddEntryHandler(input_adapter, output_adapter, TinyDbDriver())
    return handler


@click.command()
@click.option('--title', default="n/a", help='the title of a to-read entry')
@click.option('--url', help='the url of a to-read entry')
def add_entry(title, url):
    handler = create_add_entry_handler()
    handler.handle({'title': title, 'url': url})


if __name__ == "__main__":
    add_entry()
