from pyworkflow.node import VizNode, NodeException
from pyworkflow.parameters import *

import pandas as pd
import altair as alt


class GraphNode(VizNode):
    """Displays a pandas DataFrame in a visual graph.

    Raises:
        NodeException: any error generating Altair Chart.
    """
    name = "Graph Node"
    num_in = 1
    num_out = 0

    OPTIONS = {
        "graph_type": SelectParameter(
            "Graph Type",
            options=["area", "bar", "line", "point"],
            default="bar",
            docstring="Graph viz type"
        ),
        "mark_options": BooleanParameter(
            "Specify mark options",
            default=False,
            docstring="Specify mark options"
        ),
        "width": IntegerParameter(
            "Mark width",
            default=10,
            docstring="Width of marks"
        ),
        "height": IntegerParameter(
            "Mark height",
            default=10,
            docstring="Height of marks"
        ),
        "encode_options": BooleanParameter(
            "Specify encoding options",
            default=True,
            docstring="Specify encoding options"
        ),
        "x_axis": StringParameter(
            "X-Axis",
            default="a",
            docstring="X-axis values"
        ),
        "y_axis": StringParameter(
            "Y-Axis",
            default="average(b)",
            docstring="Y-axis values"
        )
    }

    def execute(self, predecessor_data, flow_vars):
        try:
            df = pd.DataFrame.from_dict(predecessor_data[0])

            if flow_vars["mark_options"].get_value():
                mark_options = {
                    "height": flow_vars["height"].get_value(),
                    "width": flow_vars["width"].get_value(),
                }
            else:
                mark_options = {}

            if flow_vars["encode_options"].get_value():
                encode_options = {
                    "x": flow_vars["x_axis"].get_value(),
                    "y": flow_vars["y_axis"].get_value(),
                }
            else:
                encode_options = {}

            graph_type = flow_vars["graph_type"].get_value()

            # Generate requested chart with options
            if graph_type == "area":
                chart = alt.Chart(df).mark_area(**mark_options).encode(**encode_options)
            elif graph_type == "bar":
                chart = alt.Chart(df).mark_bar(**mark_options).encode(**encode_options)
            elif graph_type == "line":
                chart = alt.Chart(df).mark_line(**mark_options).encode(**encode_options)
            elif graph_type == "point":
                chart = alt.Chart(df).mark_point(**mark_options).encode(**encode_options)
            else:
                chart = None

            return chart.to_json()
        except Exception as e:
            print(e)
            raise NodeException('graph node', str(e))
