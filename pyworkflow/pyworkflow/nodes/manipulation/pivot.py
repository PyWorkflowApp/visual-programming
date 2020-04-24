from pyworkflow.node import ManipulationNode, NodeException
from pyworkflow.parameters import *

import pandas as pd


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
            input_df = pd.DataFrame.from_dict(predecessor_data[0])
            output_df = pd.DataFrame.pivot_table(input_df, **self.options)
            return output_df.to_json()
        except Exception as e:
            raise NodeException('pivot', str(e))
