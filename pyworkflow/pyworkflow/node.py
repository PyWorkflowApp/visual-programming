from .parameters import *


class Node:
    """Node object

    """
    options = Options()
    option_types = OptionTypes()

    def __init__(self, node_info):
        self.name = node_info.get('name')
        self.node_id = node_info.get('node_id')
        self.node_type = node_info.get('node_type')
        self.node_key = node_info.get('node_key')
        self.data = node_info.get('data')
        self.filename = node_info.get('filename')
        self.is_global = node_info.get('is_global') is True

        self.option_values = dict()
        if node_info.get("options"):
            self.option_values.update(node_info["options"])

        self.option_replace = dict()
        if node_info.get("option_replace"):
            self.option_replace.update(node_info["option_replace"])

    def execute(self, predecessor_data, flow_vars):
        raise NotImplementedError()

    def get_execution_options(self, workflow, flow_nodes):
        """Replace Node options with flow variables.

        If the user has specified any flow variables to replace Node options,
        perform the replacement and return a dict with all options to use for
        execution. If no flow variables are included, this method will return
        a copy of all Node options.

        For any 'file' options, the value will be replaced with a path based on
        the Workflow's root directory.

        Args:
            workflow: Workflow object to construct file paths
            flow_nodes: dict of FlowNodes used to replace options

        Returns:
            dict containing options to use for execution
        """
        execution_options = dict()

        # TODO: Can we iterate through flow_vars instead?
        #       If none are included, we can just return `self.options`.
        for key, option in self.options.items():

            if key in flow_nodes:
                replacement_value = flow_nodes[key].get_replacement_value()
            else:
                replacement_value = option.get_value()

            if key == 'file':
                option.set_value(workflow.path(replacement_value))
            else:
                option.set_value(replacement_value)

            execution_options[key] = option

        return execution_options

    def validate(self):
        """Validate Node configuration

        Checks all Node options and validates all Parameter classes using
        their validation method.

        Raises:
            ParameterValidationError: invalid Parameter value
        """
        for key, option in self.options.items():
            if key not in self.option_replace:
                option.validate()

    def validate_input_data(self, num_input_data):
        """Validate Node input data.

        Checks that input data, if any, matches with required number of input
        ports.

        Args:
            num_input_data: Number of input data passed in

        Raises:
            NodeException on mis-matched input ports/data
        """
        if num_input_data != self.num_in:
            raise NodeException(
                'execute',
                f'{self.node_key} requires {self.num_in} inputs. {num_input_data} were provided'
            )

    def to_json(self):
        return {
            "name": self.name,
            "node_id": self.node_id,
            "node_type": self.node_type,
            "node_key": self.node_key,
            "data": self.data,
            "is_global": self.is_global,
            "option_values": self.option_values,
            "option_replace": self.option_replace,
        }

    def __str__(self):
        return "Test"


class FlowNode(Node):
    """FlowNodes object.

    FlowNodes do not execute. They specify a variable name and value to pass
    to other Nodes as a way to dynamically change other parameter values.
    """
    display_name = "Flow Control"

    def execute(self, predecessor_data, flow_vars):
        return

    def get_replacement_value(self):
        return self.options['default_value'].get_value()


class IONode(Node):
    """IONodes deal with file-handling in/out of the Workflow."""
    color = "green"

    def execute(self, predecessor_data, flow_vars):
        raise NotImplementedError()


class ManipulationNode(Node):
    """ManipulationNodes deal with data manipulation."""
    color = "goldenrod"

    def execute(self, predecessor_data, flow_vars):
        raise NotImplementedError()


class VizNode(Node):
    """VizNodes deal with graphical display of data."""
    color = "red"

    def execute(self, predecessor_data, flow_vars):
        raise NotImplementedError()


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
