import click

from pyworkflow import Workflow
from pyworkflow import NodeException


class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--file-directory', type=click.Path())
@pass_config
def cli(config, file_directory):
    if file_directory is None:
        file_directory = '.'
    config.file_directory = file_directory


@cli.command()
@pass_config
def execute(config):
    try:
        click.echo('Loading workflow file form %s' % config.file_directory)
        Workflow.execute_workflow(config.file_directory)
    except NodeException as ne:
        click.echo("Issues during node exception")
        click.echo(ne)
