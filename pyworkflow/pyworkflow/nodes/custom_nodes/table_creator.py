from pyworkflow.node import IONode, NodeException
from pyworkflow.parameters import *

import pandas as pd
import io


class TableCreatorNode(IONode):
    """Accepts raw-text CSV input to create data tables.

    Raises:
         NodeException: any error reading CSV file, converting
            to DataFrame.
    """
    name = "Table Creator"
    num_in = 0
    num_out = 1

    OPTIONS = {
        "input": TextParameter(
            "Input",
            default="",
            docstring="Text input"
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
            df = pd.read_csv(
                io.StringIO(flow_vars["input"].get_value()),
                sep=flow_vars["sep"].get_value(),
                header=flow_vars["header"].get_value()
            )
            return df.to_json()
        except Exception as e:
            raise NodeException('read csv', str(e))
