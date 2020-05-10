import unittest
from pyworkflow import *
import networkx as nx
from pyworkflow.tests.sample_test_data import GOOD_PARAMETERS, BAD_PARAMETERS


class ParameterTestCase(unittest.TestCase):
    def test_string_param(self):
        full_json = {
            'type': 'string',
            'label': 'Index',
            'value': 'my value',
            'docstring': 'my docstring'
        }

        self.assertDictEqual(GOOD_PARAMETERS["string_param"].to_json(), full_json)

    def test_parameter_validate_not_implemented(self):
        test_param = Parameter(dict())
        params = [test_param]

        for param_to_validate in params:
            with self.assertRaises(NotImplementedError):
                param_to_validate.validate()

    def test_validate_string_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_string_param"].validate()

    def test_validate_integer_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_int_param"].validate()

    def test_validate_boolean_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_bool_param"].validate()

    def test_validate_text_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_text_param"].validate()

    def test_validate_select_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_select_param"].validate()

    def test_validate_file_param(self):
        with self.assertRaises(ParameterValidationError):
            BAD_PARAMETERS["bad_file_param"].validate()

    def test_parameter_validation_error(self):
        try:
            BAD_PARAMETERS["bad_string_param"].validate()
        except ParameterValidationError as e:
            self.assertEqual(str(e), "Invalid value '42' (type 'int') for StringParameter")

