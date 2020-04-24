from pyworkflow.node import ManipulationNode, NodeException
from pyworkflow.parameters import *

import pandas as pd


class JoinNode(ManipulationNode):
    name = "Joiner"
    num_in = 2
    num_out = 1

    OPTIONS = {
        "on": StringParameter("Join Column", docstring="Name of column to join on")
    }

    def execute(self, predecessor_data, flow_vars):
        try:
            first_df = pd.DataFrame.from_dict(predecessor_data[0])
            second_df = pd.DataFrame.from_dict(predecessor_data[1])
            combined_df = pd.merge(
                first_df,
                second_df,
                on=flow_vars["on"].get_value()
            )
            return combined_df.to_json()
        except Exception as e:
            raise NodeException('join', str(e))
