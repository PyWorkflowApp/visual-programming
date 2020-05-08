import React, { useState } from 'react';
import { Dropdown, ButtonGroup, Table } from 'react-bootstrap';
import CustomNodeModel from './CustomNode/CustomNodeModel';
import NodeConfig from './CustomNode/NodeConfig';
import * as API from '../API';


export default class GlobalFlowMenu extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
        show: false,
        activeNode: null,
        creating: false
      }
    };

    toggleShow = () => {
      this.setState({ show: !this.state.show});
    };

    // Create CustomNodeModel from JSON data,
    // whether from menu item or global flow variable
    nodeFromData = (data) => {
        const info = {...data, is_global: true};
        const config = info.options;
        delete info.options;
        if (!info.option_types) {
            info.option_types = this.lookupOptionTypes(info.node_key);
        }

        const node = new CustomNodeModel(info, config);
        return node;
    };

    // Look up option types from appropriate menu item.
    // The option types aren't included in the global flow
    // serialization from the server.
    lookupOptionTypes = (nodeKey) => {
        const keyMatches = this.props.menuItems.filter(d => d.node_key === nodeKey);
        if (!keyMatches.length) {
          return {};
        }

        return keyMatches[0].option_types || {};
    };

    handleEdit = (data, create = false) => {
        const node = this.nodeFromData(data);
        this.setState({ creating: create, show: true, activeNode: node});
    };

    handleSubmit = (data) => {
        const node = this.state.activeNode;
        if (this.state.creating) {
            node.config = data;
            API.addNode(node)
                .then(() => this.props.onUpdate())
                .catch(err => console.log(err));
        } else {
            API.updateNode(node, data)
                .then(() => this.props.onUpdate())
                .catch(err => console.log(err));
        }
    };

    handleDelete = (data) => {
        const msg = "Are you sure you want to delete the global flow variable?";
        if (window.confirm(msg)) {
            const node = this.nodeFromData(data)
            API.deleteNode(node)
                .then(() => this.props.onUpdate())
                .catch(err => console.log(err));
        }
    };

    render() {
      return (
          <div className="GlobalFlowMenu">
              <h3>Flow Variables</h3>
              <Table size="sm">
                  <thead>
                      <tr>
                          <th>Name</th>
                          <th>Type</th>
                          <th>Value</th>
                          <th></th>
                          <th></th>
                      </tr>
                  </thead>
                  <tbody>
                  {this.props.nodes.map(node =>
                      <tr key={node.id}>
                          <td>{node.options.var_name}</td>
                          <td>{node.name}</td>
                          <td className="text-primary">{node.options.default_value}</td>
                          <td className="edit-global" title="Edit Variable"
                              onClick={() => this.handleEdit(node, false)}>
                              &#x270E;
                          </td>
                          <td className="delete-global" title="Delete Variable"
                              onClick={() => this.handleDelete(node)}>
                              x
                          </td>
                      </tr>
                  )}

                  </tbody>
              </Table>
              <Dropdown as={ButtonGroup}>
                  <Dropdown.Toggle split variant="success" size="sm" id="dropdown-split-basic">
                      Add Global Flow Variable&nbsp;
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                      {this.props.menuItems.map((node, i) =>
                          <Dropdown.Item key={node.key || i}
                                         onClick={() => this.handleEdit(node, true)}>
                              {node.name}
                          </Dropdown.Item>
                      )}
                  </Dropdown.Menu>
              </Dropdown>
              <NodeConfig node={this.state.activeNode}
                          show={this.state.show} toggleShow={this.toggleShow}
                          onSubmit={this.handleSubmit} />
          </div>
      );
    };
}
