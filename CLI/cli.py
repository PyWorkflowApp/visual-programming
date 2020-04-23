import sys

import click
import os
import uuid

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
    config.file_directory = file_directory

    stdin_files = []

    if not click.get_text_stream('stdin').isatty():

        stdin_text = click.get_text_stream('stdin')

        # TODO should be done for each separate file coming from stdin, currently working for one file, but easy to build up.

        #write standard in to a new file in local filesystem
        file_name = str(uuid.uuid4())

        # TODO small issue here, might be better to upload this file to the workflow directory instead of cwd
        new_file_path = os.path.join(os.getcwd(), file_name)

        #read from std in and upload a new file in project directory
        with open(new_file_path, 'w') as f:
            f.write(stdin_text.read())

        stdin_files.append(file_name)

    config.stdin_files = stdin_files


@cli.command()
@pass_config
def execute(config):
    if config.file_directory is None:
        click.echo('Please specify a workflow to run')
        return
    try:
        click.echo('Loading workflow file form %s' % config.file_directory)
        Workflow.execute_workflow(config.file_directory, config.stdin_files)
    except NodeException as ne:
        click.echo("Issues during node execution")
        click.echo(ne)
