import React, { useState } from 'react';
import { Dropdown, ButtonGroup, Table } from 'react-bootstrap';
import CustomNodeModel from './CustomNode/CustomNodeModel';
import NodeConfig from './CustomNode/NodeConfig';
import * as API from '../API';


export default function GlobalFlowMenu(props) {
    const [show, setShow] = useState(false);
    const [activeNode, setActiveNode] = useState();
    const [creating, setCreating] = useState(false);
    const toggleShow = () => setShow(!show);

    // Create CustomNodeModel from JSON data,
    // whether from menu item or global flow variable
    function nodeFromData(data) {
        const info = {...data, is_global: true};
        const config = info.options;
        delete info.options;
        if (!info.option_types) {
            info.option_types = lookupOptionTypes(info.node_key);
        }
        const node = new CustomNodeModel(info, config);
        return node;
    }

    // Look up option types from appropriate menu item.
    // The option types aren't included in the global flow
    // serialization from the server.
    function lookupOptionTypes(nodeKey) {
        const keyMatches = props.menuItems.filter(d => d.node_key === nodeKey);
        if (!keyMatches.length) return {};
        return keyMatches[0].option_types || {};
    }

    const handleEdit = (data, create = false) => {
        setCreating(create);
        const node = nodeFromData(data);
        setActiveNode(node);
        setShow(true);
    };

    const handleSubmit = (data) => {
        const node = activeNode;
        if (creating) {
            node.config = data;
            API.addNode(node)
                .then(() => props.onUpdate())
                .catch(err => console.log(err));
        } else {
            API.updateNode(node, data)
                .then(() => props.onUpdate())
                .catch(err => console.log(err));
        }
    };

    const handleDelete = (data) => {
        const msg = "Are you sure you want to delete the global flow variable?";
        if (window.confirm(msg)) {
            const node = nodeFromData(data)
            API.deleteNode(node)
                .then(() => props.onUpdate())
                .catch(err => console.log(err));
        }
    };

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
                {props.nodes.map(node =>
                    <tr key={node.id}>
                        <td>{node.options.var_name}</td>
                        <td>{node.name}</td>
                        <td className="text-primary">{node.options.default_value}</td>
                        <td className="edit-global" title="Edit Variable"
                            onClick={() => handleEdit(node, false)}>
                            &#x270E;
                        </td>
                        <td className="delete-global" title="Delete Variable"
                            onClick={() => handleDelete(node)}>
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
                    {props.menuItems.map((node, i) =>
                        <Dropdown.Item key={node.key || i}
                                       onClick={() => handleEdit(node, true)}>
                            {node.name}
                        </Dropdown.Item>
                    )}
                </Dropdown.Menu>
            </Dropdown>
            <NodeConfig node={activeNode}
                        show={show} toggleShow={toggleShow}
                        onSubmit={handleSubmit} />
        </div>
    )
}


