from typing import List
import click

from reading_list.core.application.commands import AddEntryCommandHandler, ListEntriesCommandHandler
from reading_list.core.application.inputs import InputEventFactory
from reading_list.core.dependencies.bootstrapper import ADependencyInjectionBootstrapper, NaiveDependencyInjectionBootstrapper
from reading_list.core.dependencies.dependency_injection import ADependencyInjectionContainer, NaiveDependencyInjectionContainer
from reading_list.core.domain.entities import ReadingEntry
from reading_list.shared.config import AConfig, DEFAULT_CONFIGS, initialize_custom_configs


class AppStarter:
    def __init__(self) -> None:
        self.di_container: ADependencyInjectionContainer = NaiveDependencyInjectionContainer()
        self.di_bootstrapper: ADependencyInjectionBootstrapper = NaiveDependencyInjectionBootstrapper(
            self.di_container)

    def setup_di_with_configs(self, configs: AConfig) -> None:
        self.di_container = self.di_bootstrapper.bootstrap_with_configurations(
            configs)


APP_STARTER = AppStarter()


@click.group()
@click.option('-C', '--configuration',
              help='Path to a configuration JSON file')
def cli(configuration: str) -> None:
    if configuration:
        configs = initialize_custom_configs(configuration)
        APP_STARTER.setup_di_with_configs(configs)
    else:
        APP_STARTER.setup_di_with_configs(DEFAULT_CONFIGS)


@cli.command()
@click.option('-t', '--title', required=True,
              help='Title of the reading entry')
@click.option('-l', '--link',
              help='Link to the reading entry')
def add(title: str, link: str) -> None:
    data = InputEventFactory.make_data_input_event(dict(
        title=title, link=link or ''))
    handler = AddEntryCommandHandler(APP_STARTER.di_container)
    result = handler.handle(data)
    if result.is_ok():
        click.echo('Ok.')
    else:
        click.echo('Could not add an entry.', err=True)


@cli.command()
def list() -> None:
    data = InputEventFactory.make_data_input_event({})
    handler = ListEntriesCommandHandler(APP_STARTER.di_container)
    result = handler.handle(data)
    if result.is_ok():
        entries: List[ReadingEntry] = result.data['entries'] or []
        for entry in entries:
            click.echo(f'-> {entry.title} @ {entry.link or "_"}')
    else:
        click.echo('Could not retrieve entries.', err=True)


if __name__ == '__main__':
    cli()
