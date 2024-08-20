from pyworkflow.node import ManipulationNode, NodeException
from pyworkflow.parameters import *

import pandas as pd


class PivotNode(ManipulationNode):
    """Create a spreadsheet-style pivot table as a DataFrame.

    pandas reference:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html

    Raises:
        NodeException: catches exceptions when dealing with pandas DataFrames.
    """
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
            input_df = pd.DataFrame.from_dict(predecessor_data[0])
            output_df = pd.DataFrame.pivot_table(
                input_df,
                index=flow_vars['index'].get_value(),
                values=flow_vars['values'].get_value(),
                columns=flow_vars['columns'].get_value(),
                aggfunc=flow_vars['aggfunc'].get_value(),
                fill_value=flow_vars['fill_value'].get_value(),
                margins=flow_vars['margins'].get_value(),
                dropna=flow_vars['dropna'].get_value(),
                margins_name=flow_vars['margins_name'].get_value(),
                observed=flow_vars['observed'].get_value(),
            )
            return output_df.to_json()
        except Exception as e:
            raise NodeException('pivot', str(e))
