from pyworkflow.node import IONode, NodeException
from pyworkflow.parameters import *

import pandas as pd


class WriteCsvNode(IONode):
    """Writes the current DataFrame to a CSV file.

    Raises:
        NodeException: any error writing CSV file, converting from DataFrame.
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
            # Convert JSON data to DataFrame
            df = pd.DataFrame.from_dict(predecessor_data[0])

            # Write to CSV and save
            df.to_csv(
                flow_vars["file"].get_value(),
                sep=flow_vars["sep"].get_value(),
                index=flow_vars["index"].get_value()
            )
            return df.to_json()
        except Exception as e:
            raise NodeException('write csv', str(e))
