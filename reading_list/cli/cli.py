# TODO:
# 1. build click command runtime for adding new reading list entries
# 2. refactor dependency injection bootstrapping
# 3. implement the click command runtime for listing list entries
import click

from reading_list.core.application.commands import AddEntryCommandHandler
from reading_list.core.application.inputs import InputEventFactory
from reading_list.core.application.results import AResult
from reading_list.core.dependencies.bootstrapper import NaiveBootstrapper
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer, NaiveDependencyInjectionContainer

di_container: ADependencyInjectionContainer = NaiveDependencyInjectionContainer()
di_container = NaiveBootstrapper(di_container).bootstrap_di()


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('-t', '--title', required=True,
              help="Title of the reading entry")
@click.option('-l', '--link',
              help="Link to the reading entry")
def add(title: str, link: str) -> None:
    data = InputEventFactory.make_data_input_event(
        dict(title=title, link=link or ''))
    handler = AddEntryCommandHandler(di_container)
    result: AResult = handler.handle(data)
    click.echo('Ok.' if result.is_ok() else 'Could not add an entry.')


if __name__ == '__main__':
    cli()
