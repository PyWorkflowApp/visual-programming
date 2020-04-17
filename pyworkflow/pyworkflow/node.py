import pandas as pd

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

        self.is_global = node_info.get('is_global') is True

        self.option_values = dict()
        if node_info.get("options"):
            self.option_values.update(node_info["options"])

    def execute(self, predecessor_data, flow_vars):
        pass

    def validate(self):
        return True

    def __str__(self):
        return "Test"


class FlowNode(Node):
    """FlowNode object
    """
    display_name = "Flow Control"


class StringNode(FlowNode):
    """StringNode object

    Allows for Strings to replace 'string' fields in Nodes
    """
    name = "String Input"
    num_in = 1
    num_out = 1
    color = 'purple'

    OPTIONS = {
        "default_value": StringParameter(
            "Default Value",
            docstring="Value this node will pass as a flow variable"
        ),
        "var_name": StringParameter(
            "Variable Name",
            default="my_var",
            docstring="Name of the variable to use in another Node"
        )
    }


class IONode(Node):
    """IONodes deal with file-handling in/out of the Workflow.

    Possible types:
        Read CSV
        Write CSV
    """
    color = 'black'
    display_name = "I/O"

    def execute(self, predecessor_data, flow_vars):
        pass

    def validate(self):
        return True


class ReadCsvNode(IONode):
    """ReadCsvNode

    Reads a CSV file into a pandas DataFrame.

    Raises:
         NodeException: any error reading CSV file, converting
            to DataFrame.
    """
    name = "Read CSV"
    num_in = 0
    num_out = 1

    OPTIONS = {
        "file": FileParameter(
            "File",
            docstring="CSV File"
        ),
        "sep": StringParameter(
            "Delimiter",
            default=",",
            docstring="Column delimiter"
        ),
        # user-specified headers are probably integers, but haven't figured out
        # arguments with multiple possible types
        "header": StringParameter(
            "Header Row",
            default="infer",
            docstring="Row number containing column names (0-indexed)"
        ),
    }

    def execute(self, predecessor_data, flow_vars):
        try:
            # Read CSV needs exactly 0 input DataFrame
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
            NodeUtils.replace_flow_vars(self.options, flow_vars)
            fname = self.options["file"].get_value()
            sep = self.options["sep"].get_value()
            hdr = self.options["header"].get_value()
            df = pd.read_csv(fname, sep=sep, header=hdr)
            return df.to_json()
        except Exception as e:
            raise NodeException('read csv', str(e))

    def __str__(self):
        return "ReadCsvNode"


class WriteCsvNode(IONode):
    """WriteCsvNode

    Writes the current DataFrame to a CSV file.

    Raises:
        NodeException: any error writing CSV file, converting
            from DataFrame.
    """
    name = "Write CSV"
    num_in = 1
    num_out = 0
    download_result = True

    OPTIONS = {
        "file": StringParameter(
            "Filename",
            docstring="CSV file to write"
        ),
        "sep": StringParameter(
            "Delimiter",
            default=",",
            docstring="Column delimiter"
        ),
        "index": BooleanParameter(
            "Write Index",
            default=True,
            docstring="Write index as column?"
        ),
    }

    def execute(self, predecessor_data, flow_vars):
        try:
            # Write CSV needs exactly 1 input DataFrame
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)

            # Convert JSON data to DataFrame
            df = pd.DataFrame.from_dict(predecessor_data[0])

            # Write to CSV and save
            fname = self.options["file"].get_value()
            sep = self.options["sep"].get_value()
            index = self.options["index"].get_value()
            df.to_csv(fname, sep=sep, index=index)
            return df.to_json()
        except Exception as e:
            raise NodeException('write csv', str(e))


class ManipulationNode(Node):
    """ManipulationNodes deal with data manipulation.

    Possible types:
        Pivot
        Filter
        Multi-in
    """
    display_name = "Manipulation"
    color = 'goldenrod'

    def execute(self, predecessor_data, flow_vars):
        pass

    def validate(self):
        return True


class PivotNode(ManipulationNode):
    name = "Pivoting"
    num_in = 1
    num_out = 3

    OPTIONS = {
        'index': StringParameter(
            'Index',
            docstring='Column to aggregate (column, grouper, array or list)'
        ),
        'values': StringParameter(
            'Values',
            docstring='Column name to use to populate new frame\'s values (column, grouper, array or list)'
        ),
        'columns': StringParameter(
            'Column Name Row',
            docstring='Column(s) to use for populating new frame values. (column, grouper, array or list)'
        ),
        'aggfunc': StringParameter(
            'Aggregation function',
            default='mean',
            docstring='Function used for aggregation (function, list of functions, dict, default numpy.mean)'
        ),
        'fill_value': StringParameter(
            'Fill value',
            docstring='Value to replace missing values with (scalar)'
        ),
        'margins': BooleanParameter(
            'Margins name',
            default=False,
            docstring='Add all rows/columns'
        ),
        'dropna': BooleanParameter(
            'Drop NaN columns',
            default=True,
            docstring='Ignore columns with all NaN entries'
        ),
        'margins_name': StringParameter(
            'Margins name',
            default='All',
            docstring='Name of the row/column that will contain the totals when margins is True'
        ),
        'observed': BooleanParameter(
            'Column Name Row',
            default=False,
            docstring='Row number with column names (0-indexed) or "infer"'
        )
    }

    def execute(self, predecessor_data, flow_vars):
        try:
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
            input_df = pd.DataFrame.from_dict(predecessor_data[0])
            output_df = pd.DataFrame.pivot_table(input_df, **self.options)
            return output_df.to_json()
        except Exception as e:
            raise NodeException('pivot', str(e))


class JoinNode(ManipulationNode):
    name = "Joiner"
    num_in = 2
    num_out = 1

    OPTIONS = {
        "on": StringParameter("Join Column", docstring="Name of column to join on")
    }

    def execute(self, predecessor_data, flow_vars):
        # Join cannot accept more than 2 input DataFrames
        # TODO: Add more error-checking if 1, or no, DataFrames passed through
        try:
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
            first_df = pd.DataFrame.from_dict(predecessor_data[0])
            second_df = pd.DataFrame.from_dict(predecessor_data[1])
            combined_df = pd.merge(first_df, second_df,
                                   on=self.options["on"].get_value())
            return combined_df.to_json()
        except Exception as e:
            raise NodeException('join', str(e))


class FilterNode(ManipulationNode):
    name = "Filter"
    num_in = 1
    num_out = 1

    OPTIONS = {
        'items': StringParameter(
            'Items',
            docstring='Keep labels from axis which are in items'
        ),
        'like': StringParameter(
            'Like',
            docstring='Keep labels from axis for which like in label == True.'
        ),
        'regex': StringParameter(
            'Regex',
            docstring='Keep labels from axis for which re.search(regex, label) == True.'
        ),
        'axis': StringParameter(
            'Axis',
            docstring='The axis to filter on.'
        )
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data, flow_vars):
        try:
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
            input_df = pd.DataFrame.from_dict(predecessor_data[0])
            output_df = pd.DataFrame.filter(input_df, **self.options)
            return output_df.to_json()
        except Exception as e:
            raise NodeException('filter', str(e))


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason


class NodeUtils:

    FIXED_INPUT_NODES = ['WriteCsvNode', 'FilterNode', 'JoinNode'] # nodes which can only have a fixed number of predecessors
    MAX_INPUT_NODES = ['ReadCsvNode'] # nodes for which num_in represents a maximum number of predecessors

    @staticmethod
    def validate_predecessor_data(predecessor_data_len, num_in, node_key):
        validation_failed = False
        exception_txt = ""
        if node_key in NodeUtils.FIXED_INPUT_NODES and predecessor_data_len != num_in:
                validation_failed = True
                exception_txt = '%s needs %d inputs. %d were provided'
        elif (node_key in NodeUtils.MAX_INPUT_NODES and predecessor_data_len > num_in):
                validation_failed = True
                exception_txt = '%s can take up to %d inputs. %d were provided'

        if validation_failed:
            raise NodeException(
                'execute',
                exception_txt % (node_key, num_in, predecessor_data_len)
            )

    @staticmethod
    def replace_flow_vars(node_options, flow_vars):
        # TODO: this will no longer work with the Node.options descriptor,
        #       which uses Node.option_values to populate the Parameter
        #       class values upon access
        for var in flow_vars:
            node_options[var['var_name']] = var['default_value']

        return
