from pyworkflow.node import IONode, NodeException
from pyworkflow.parameters import *

import pandas as pd


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
            df = pd.read_csv(
                flow_vars["file"].get_value(),
                sep=flow_vars["sep"].get_value(),
                header=flow_vars["header"].get_value()
            )
            return df.to_json()
        except Exception as e:
            raise NodeException('read csv', str(e))

    def execute_for_read(self, predecessor_data, flow_vars, file_to_read):
        try:
            fname = file_to_read
            sep = self.options["sep"].get_value()
            hdr = self.options["header"].get_value()
            df = pd.read_csv(fname, sep=sep, header=hdr)
            return df.to_json()
        except Exception as e:
            raise NodeException('read csv', str(e))