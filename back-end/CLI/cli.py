import click
import json

from pyworkflow import Workflow, WorkflowException
from pyworkflow import NodeException
from pyworkflow.nodes import ReadCsvNode, WriteCsvNode


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filenames', type=click.Path(exists=True), nargs=-1)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
def execute(filenames, verbose):
    """Execute Workflow file(s)."""
    # Check whether to log to terminal, or redirect output
    log = click.get_text_stream('stdout').isatty()

    # Execute each workflow in the args
    for workflow_file in filenames:

        if workflow_file is None:
            click.echo('Please specify a workflow to run', err=True)
            return

        if log:
            click.echo('Loading workflow file from %s' % workflow_file)

        try:
            workflow = open_workflow(workflow_file)
            execute_workflow(workflow, log, verbose)
        except OSError as e:
            click.echo(f"Issues loading workflow file: {e}", err=True)
        except WorkflowException as e:
            click.echo(f"Issues during workflow execution\n{e}", err=True)


def execute_workflow(workflow, log, verbose):
    """Execute a workflow file, node-by-node.

    Retrieves the execution order from the Workflow and iterates through nodes.
    If any I/O nodes are present AND stdin/stdout redirection is provided in the
    command-line, overwrite the stored options and then replace before saving.

    Args:
        workflow - Workflow object loaded from file
        log - True, for outputting to terminal; False for stdout redirection
        verbose - True, for outputting debug information; False otherwise
    """
    execution_order = workflow.execution_order()

    # Execute each node in the order returned by the Workflow
    for node in execution_order:
        try:
            node_to_execute = workflow.get_node(node)
            original_file_option = pre_execute(workflow, node_to_execute, log)

            if verbose:
                print('Executing node of type ' + str(type(node_to_execute)))

            # perform execution
            executed_node = workflow.execute(node)

            # If file was replaced with stdin/stdout, restore original option
            if original_file_option is not None:
                executed_node.option_values["file"] = original_file_option

            # Update Node in Workflow with changes (saved data file)
            workflow.update_or_add_node(executed_node)
        except NodeException as e:
            click.echo(f"Issues during node execution\n{e}", err=True)

    if verbose:
        click.echo('Completed workflow execution!')


def pre_execute(workflow, node_to_execute, log):
    """Pre-execution steps, to overwrite file options with stdin/stdout.

    If stdin is not a tty, and the Node is ReadCsv, replace file with buffer.
    If stdout is not a tty, and the Node is WriteCsv, replace file with buffer.

    Args:
        workflow - Workflow object loaded from file
        node_to_execute - The Node to execute
        log - True, for outputting to terminal; False for stdout redirection
    """
    stdin = click.get_text_stream('stdin')

    if type(node_to_execute) is ReadCsvNode and not stdin.isatty():
        new_file_location = stdin
    elif type(node_to_execute) is WriteCsvNode and not log:
        new_file_location = click.get_text_stream('stdout')
    else:
        # No file redirection needed
        return None

    # save original file info
    original_file_option = node_to_execute.option_values["file"]

    # replace with value from stdin and save
    node_to_execute.option_values["file"] = new_file_location
    workflow.update_or_add_node(node_to_execute)

    return original_file_option


def open_workflow(workflow_file):
    with open(workflow_file) as f:
        json_content = json.load(f)

    return Workflow.from_json(json_content['pyworkflow'])
