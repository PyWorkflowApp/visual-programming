import React from 'react'
import { shallow, mount } from 'enzyme';
import { render } from '@testing-library/react'
import { DiagramModel } from '@projectstorm/react-diagrams';
import GlobalFlowMenu from '../../src/components/GlobalFlowMenu';

global.confirm = () => true;
global.console = {log: jest.fn(() => []), error: jest.fn(() => [])}

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

const nodes = {"Visualization": [{"name": "Graph Node", "node_key": "GraphNode", "node_type": "visualization", "num_in": 1, "num_out": 0, "color": "red", "filename": "graph", "doc": "Displays a pandas DataFrame in a visual graph.\n\n    Raises:\n        NodeException: any error generating Altair Chart.\n    ", "options": {"graph_type": "bar", "mark_options": false, "width": 10, "height": 10, "encode_options": true, "x_axis": "a", "y_axis": "average(b)"}, "option_types": {"graph_type": {"type": "select", "label": "Graph Type", "value": "bar", "docstring": "Graph viz type", "options": ["area", "bar", "line", "point"]}, "mark_options": {"type": "boolean", "label": "Specify mark options", "value": false, "docstring": "Specify mark options"}, "width": {"type": "int", "label": "Mark width", "value": 10, "docstring": "Width of marks"}, "height": {"type": "int", "label": "Mark height", "value": 10, "docstring": "Height of marks"}, "encode_options": {"type": "boolean", "label": "Specify encoding options", "value": true, "docstring": "Specify encoding options"}, "x_axis": {"type": "string", "label": "X-Axis", "value": "a", "docstring": "X-axis values"}, "y_axis": {"type": "string", "label": "Y-Axis", "value": "average(b)", "docstring": "Y-axis values"}}, "download_result": false}], "Flow Control": [{"name": "Integer Input", "node_key": "IntegerNode", "node_type": "flow_control", "num_in": 1, "num_out": 1, "color": "purple", "filename": "integer_input", "doc": "StringNode object\n\n    Allows for Strings to replace 'string' fields in Nodes\n    ", "options": {"default_value": null, "var_name": "my_var"}, "option_types": {"default_value": {"type": "int", "label": "Default Value", "value": null, "docstring": "Value this node will pass as a flow variable"}, "var_name": {"type": "string", "label": "Variable Name", "value": "my_var", "docstring": "Name of the variable to use in another Node"}}, "download_result": false}, {"name": "String Input", "node_key": "StringNode", "node_type": "flow_control", "num_in": 1, "num_out": 1, "color": "purple", "filename": "string_input", "doc": "StringNode object\n\n    Allows for Strings to replace 'string' fields in Nodes\n    ", "options": {"default_value": null, "var_name": "my_var"}, "option_types": {"default_value": {"type": "string", "label": "Default Value", "value": null, "docstring": "Value this node will pass as a flow variable"}, "var_name": {"type": "string", "label": "Variable Name", "value": "my_var", "docstring": "Name of the variable to use in another Node"}}, "download_result": false}], "Manipulation": [{"name": "Joiner", "node_key": "JoinNode", "node_type": "manipulation", "num_in": 2, "num_out": 1, "color": "goldenrod", "filename": "join", "doc": null, "options": {"on": null}, "option_types": {"on": {"type": "string", "label": "Join Column", "value": null, "docstring": "Name of column to join on"}}, "download_result": false}, {"name": "Filter", "node_key": "FilterNode", "node_type": "manipulation", "num_in": 1, "num_out": 1, "color": "goldenrod", "filename": "filter", "doc": null, "options": {"items": null, "like": null, "regex": null, "axis": null}, "option_types": {"items": {"type": "string", "label": "Items", "value": null, "docstring": "Keep labels from axis which are in items"}, "like": {"type": "string", "label": "Like", "value": null, "docstring": "Keep labels from axis for which like in label == True."}, "regex": {"type": "string", "label": "Regex", "value": null, "docstring": "Keep labels from axis for which re.search(regex, label) == True."}, "axis": {"type": "string", "label": "Axis", "value": null, "docstring": "The axis to filter on."}}, "download_result": false}, {"name": "Pivoting", "node_key": "PivotNode", "node_type": "manipulation", "num_in": 1, "num_out": 3, "color": "goldenrod", "filename": "pivot", "doc": null, "options": {"index": null, "values": null, "columns": null, "aggfunc": "mean", "fill_value": null, "margins": false, "dropna": true, "margins_name": "All", "observed": false}, "option_types": {"index": {"type": "string", "label": "Index", "value": null, "docstring": "Column to aggregate (column, grouper, array or list)"}, "values": {"type": "string", "label": "Values", "value": null, "docstring": "Column name to use to populate new frame's values (column, grouper, array or list)"}, "columns": {"type": "string", "label": "Column Name Row", "value": null, "docstring": "Column(s) to use for populating new frame values. (column, grouper, array or list)"}, "aggfunc": {"type": "string", "label": "Aggregation function", "value": "mean", "docstring": "Function used for aggregation (function, list of functions, dict, default numpy.mean)"}, "fill_value": {"type": "string", "label": "Fill value", "value": null, "docstring": "Value to replace missing values with (scalar)"}, "margins": {"type": "boolean", "label": "Margins name", "value": false, "docstring": "Add all rows/columns"}, "dropna": {"type": "boolean", "label": "Drop NaN columns", "value": true, "docstring": "Ignore columns with all NaN entries"}, "margins_name": {"type": "string", "label": "Margins name", "value": "All", "docstring": "Name of the row/column that will contain the totals when margins is True"}, "observed": {"type": "boolean", "label": "Column Name Row", "value": false, "docstring": "Row number with column names (0-indexed) or \"infer\""}}, "download_result": false}], "I/O": [{"name": "Read CSV", "node_key": "ReadCsvNode", "node_type": "io", "num_in": 0, "num_out": 1, "color": "green", "filename": "read_csv", "doc": "ReadCsvNode\n\n    Reads a CSV file into a pandas DataFrame.\n\n    Raises:\n         NodeException: any error reading CSV file, converting\n            to DataFrame.\n    ", "options": {"file": null, "sep": ",", "header": "infer"}, "option_types": {"file": {"type": "file", "label": "File", "value": null, "docstring": "CSV File"}, "sep": {"type": "string", "label": "Delimiter", "value": ",", "docstring": "Column delimiter"}, "header": {"type": "string", "label": "Header Row", "value": "infer", "docstring": "Row number containing column names (0-indexed)"}}, "download_result": false}, {"name": "Write CSV", "node_key": "WriteCsvNode", "node_type": "io", "num_in": 1, "num_out": 0, "color": "green", "filename": "write_csv", "doc": "WriteCsvNode\n\n    Writes the current DataFrame to a CSV file.\n\n    Raises:\n        NodeException: any error writing CSV file, converting\n            from DataFrame.\n    ", "options": {"file": null, "sep": ",", "index": true}, "option_types": {"file": {"type": "string", "label": "Filename", "value": null, "docstring": "CSV file to write"}, "sep": {"type": "string", "label": "Delimiter", "value": ",", "docstring": "Column delimiter"}, "index": {"type": "boolean", "label": "Write Index", "value": true, "docstring": "Write index as column?"}}, "download_result": true}], "Custom Nodes": [{"name": "Table Creator", "node_key": "TableCreatorNode", "node_type": "custom_nodes", "num_in": 0, "num_out": 1, "color": "green", "filename": "table_creator", "doc": "Accepts raw-text CSV input to create data tables.\n\n    Raises:\n         NodeException: any error reading CSV file, converting\n            to DataFrame.\n    ", "options": {"input": "", "sep": ",", "header": "infer"}, "option_types": {"input": {"type": "text", "label": "Input", "value": "", "docstring": "Text input"}, "sep": {"type": "string", "label": "Delimiter", "value": ",", "docstring": "Column delimiter"}, "header": {"type": "string", "label": "Header Row", "value": "infer", "docstring": "Row number containing column names (0-indexed)"}}, "download_result": false}]};

const globals = [{"name": "Integer Input", "node_id": "de443b1a-4d78-4b62-93bd-e03cdaecbd02", "node_type": "flow_control", "node_key": "IntegerNode", "data": null, "filename": "integer_input", "is_global": true, "options": {"default_value": 5, "var_name": "my_var1"}, "option_replace": {}, "id": "de443b1a-4d78-4b62-93bd-e03cdaecbd02"}];


describe('Validates GlobalFlowMenu', () => {
  it('Display of GlobalFlowMenu with empty list', () => {
    const model = new DiagramModel();
    const globals = [];
    const menuItems = [];
    const getGlobalVars = jest.fn(() => []);
    const globalFlowMenu = render(<GlobalFlowMenu
                  menuItems={menuItems}
                  nodes={globals}
                  diagramModel={model}
                  onUpdate={getGlobalVars}
                  />);
    expect(globalFlowMenu).toMatchSnapshot();
  });

  it('Validates execution of methods', () => {
    const model = new DiagramModel();
    const menuItems = nodes["Flow Control"];
    const getGlobalVars = jest.fn(() => []);
    const props = {
      menuItems: menuItems,
      nodes: globals,
      diagramModel: model,
      onUpdate: getGlobalVars
    };

    const flowMenu = shallow(<GlobalFlowMenu
                  menuItems={menuItems}
                  nodes={globals}
                  diagramModel={model}
                  onUpdate={getGlobalVars}
                  />);

    flowMenu.find({ className: 'edit-global' }).simulate('click');
    expect(flowMenu.state('show')).toBe(true);

    flowMenu.find({ className: 'delete-global' }).simulate('click');

    expect(global.fetch.mock.calls.length).toBe(1);
  });
});
