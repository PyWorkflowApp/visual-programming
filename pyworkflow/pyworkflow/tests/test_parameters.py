import unittest
from pyworkflow import *
import networkx as nx


class ParameterTestCase(unittest.TestCase):
    def setUp(self):
        self.string_param = StringParameter(
            'Index',
            default='my value',
            docstring='my docstring'
        )

        self.bool_param = BooleanParameter(
            'Drop NaN columns',
            default=True,
            docstring='Ignore columns with all NaN entries'
        )

        self.file_param = FileParameter(
            "File",
            docstring="CSV File"
        )

        self.int_param = IntegerParameter(
            'Integer',
            default=42,
            docstring="CSV File"
        )

        self.bad_string_param = StringParameter(
            'Bad String',
            default=42,
            docstring="CSV File"
        )

        self.bad_int_param = StringParameter(
            'Bad Integer',
            default="foobar",
            docstring="CSV File"
        )

        self.bad_bool_param = StringParameter(
            'Bad Bool Param',
            default=42,
            docstring="CSV File"
        )

    def test_string_param(self):
        full_json = {
            'type': 'string',
            'label': 'Index',
            'value': 'my value',
            'docstring': 'my docstring'
        }

        self.assertDictEqual(self.string_param.to_json(), full_json)

    def test_validate_string_param(self):
        with self.assertRaises(ParameterValidationError):
            self.bad_string_param.validate()

    # def test_validate_integer_param(self):
    #     with self.assertRaises(ParameterValidationError):
    #         self.bad_int_param.validate()

    def test_validate_boolean_param(self):
        with self.assertRaises(ParameterValidationError):
            self.bad_bool_param.validate()

    def test_parameter_validation_error(self):
        with self.assertRaises(ParameterValidationError):
            response = self.bad_string_param.validate()
            self.assertEqual(response.__str__, "Invalid value '42' (type 'int') for StringParameter")

