import os


class Options:
    """
    Descriptor for accessing node parameters as Parameter instances

    Clones the values in the class variable `OPTIONS` and sets their values
    with the values in in the instance variable `option_values`.
    """

    def __get__(self, obj, objtype):
        # return class variable OPTIONS if invoked from class
        if obj is None:
            return getattr(objtype, "OPTIONS", dict())
        # otherwise clone class's options and set values from instance
        options = dict()
        for k, v in obj.OPTIONS.items():
            options[k] = v.clone()
        for k, v in getattr(obj, "option_values", dict()).items():
            if k in options:
                options[k].set_value(v)
        return options


class OptionTypes:
    """
    Descriptor for accessing parameter names, types, and descriptions.

    This will never reference instance parameter values, only turn the
    class OPTIONS into a dict.
    """

    def __get__(self, obj, objtype):
        # handle both instance- and class-callers
        item = obj or objtype
        if getattr(item, "OPTIONS", None) is None:
            return dict()
        return {k: v.to_json() for k, v in item.OPTIONS.items()}


class Parameter:
    type = None

    def __init__(self, label="", default=None, docstring=None):
        self._label = label
        self._value = None
        self._default = default
        self._docstring = docstring

    def clone(self):
        return self.__class__(self.label, self.default, self.docstring)

    def get_value(self):
        if self._value is None:
            return self.default
        return self._value

    def set_value(self, value):
        self._value = value

    @property
    def label(self):
        return self._label

    @property
    def default(self):
        return self._default

    @property
    def docstring(self):
        return self._docstring

    def validate(self):
        raise NotImplementedError()

    def to_json(self):
        return {
            "type": self.type,
            "label": self.label,
            "value": self.get_value(),
            "docstring": self.docstring
        }


class FileParameter(Parameter):
    type = "file"

    def validate(self):
        value = self.get_value()
        if (value is None) or (not os.path.exists(value)):
            raise ParameterValidationError(self)


class StringParameter(Parameter):
    type = "string"

    def validate(self):
        value = self.get_value()
        if not isinstance(value, str):
            raise ParameterValidationError(self)


class IntegerParameter(Parameter):
    type = "int"

    def validate(self):
        value = self.get_value()
        if not isinstance(value, int):
            raise ParameterValidationError(self)


class BooleanParameter(Parameter):
    type = "boolean"

    def validate(self):
        value = self.get_value()
        if not isinstance(value, bool):
            raise ParameterValidationError(self)


class ParameterValidationError(Exception):

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        param = self.parameter
        value = param.get_value()
        value_type = type(value).__name__
        param_type = type(param).__name__
        return f"Invalid value '{value}' (type '{value_type}') for {param_type}"
