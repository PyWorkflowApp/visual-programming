from pyworkflow.node import FlowNode, NodeException
from pyworkflow.parameters import *


class StringNode(FlowNode):
    """StringNode object

    Allows for Strings to replace 'string' fields in Nodes
    """
    name = "String Input"
    num_in = 0
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
