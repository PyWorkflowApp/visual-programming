from pyworkflow import *

GOOD_NODES = {
    "read_csv_node": {
        "name": "Read CSV",
        "node_id": "1",
        "node_type": "io",
        "node_key": "ReadCsvNode",
        "is_global": False,
        "options": {
            "file": "/tmp/sample1.csv"
        }
    },
    "write_csv_node": {
        "name": "Write CSV",
        "node_id": "2",
        "node_type": "io",
        "node_key": "WriteCsvNode",
        "is_global": False,
        "options": {
            "file": "/tmp/sample_out.csv"
        }
    },
    "join_node": {
        "name": "Joiner",
        "node_id": "3",
        "node_type": "manipulation",
        "node_key": "JoinNode",
        "is_global": False,
        "options": {
            "on": "key"
        }
    },
    "filter_node": {
        "name": "Filter",
        "node_id": "4",
        "node_type": "manipulation",
        "node_key": "FilterNode",
        "is_global": False,
        "options": {
            "on": "key"
        }
    },
    "pivot_node": {
        "name": "Pivoting",
        "node_id": "5",
        "node_type": "manipulation",
        "node_key": "PivotNode",
        "is_global": False,
        "options": {
            "on": "key"
        }
    },
    "string_input": {
        "name": "String Input",
        "node_id": "6",
        "node_type": "flow_control",
        "node_key": "StringNode",
        "is_global": False,
        "options": {
            "default_value": "My value",
            "var_name": "my_var"
        }
    },
    "global_flow_var": {
        "name": "String Input",
        "node_id": "1",
        "node_type": "flow_control",
        "node_key": "StringNode",
        "is_global": True,
        "options": {
            "default_value": "My value",
            "var_name": "my_var"
        }
    },
}

BAD_NODES = {
    "bad_flow_node": {
        "name": "Foobar",
        "node_id": "1",
        "node_type": "flow_control",
        "node_key": "foobar",
        "is_global": False,
    },
    "bad_io_node": {
        "name": "Foobar",
        "node_id": "1",
        "node_type": "io",
        "node_key": "foobar",
        "is_global": False,
    },
    "bad_manipulation_node": {
        "name": "Foobar",
        "node_id": "1",
        "node_type": "manipulation",
        "node_key": "foobar",
        "is_global": False,
    },
    "bad_node_type": {
        "name": "Foobar",
        "node_id": "1",
        "node_type": "foobar",
        "node_key": "foobar",
        "is_global": False,
    },
}

GOOD_PARAMETERS = {
    "string_param": StringParameter(
        'Index',
        default='my value',
        docstring='my docstring'
    ),
    "bool_param": BooleanParameter(
        'Drop NaN columns',
        default=True,
        docstring='Ignore columns with all NaN entries'
    ),
    "file_param": FileParameter(
        "File",
        docstring="CSV File"
    ),
    "int_param": IntegerParameter(
        'Integer',
        default=42,
        docstring="CSV File"
    ),
}

BAD_PARAMETERS = {
    "bad_string_param": StringParameter(
        'Bad String',
        default=42,
        docstring="CSV File"
    ),
    "bad_file_param": FileParameter(
        'Bad File',
        default='fobar.csv',
        docstring="CSV File"
    ),
    "bad_int_param": IntegerParameter(
        'Bad Integer',
        default="foobar",
        docstring="CSV File"
    ),
    "bad_bool_param": BooleanParameter(
        'Bad Bool Param',
        default=42,
        docstring="CSV File"
    ),
}

DATA_FILES = {
    "sample1": (',key,A\n'
                '0,K0,A0\n'
                '1,K1,A1\n'
                '2,K2,A2\n'
                '3,K3,A3\n'
                '4,K4,A4\n'
                '5,K5,A5\n'),
    "sample2": (',key,B\n'
                '0,K0,B0\n'
                '1,K1,B1\n'
                '2,K2,B2\n')
}