import React from 'react';
import * as _ from 'lodash';
import { Col } from 'react-bootstrap';


export default function NodeMenu(props) {
    // construct menu from JSON of node types
    return (
        <Col xs={2} className="node-menu">
            <div>Drag-and-drop nodes to build a workflow.</div>
            <hr />
            {_.map(props.nodes, (items, section) =>
                <div key={`node-menu-${section}`}>
                    <b>{section}</b>
                    <ul>
                        { _.map(items, item => {
                            const config = item.options;
                            delete item.options;
                            return (
                                <NodeMenuItem key={item.node_key} nodeInfo={item} config={config} />
                            )}
                        )}
                    </ul>
                </div>
            )}
        </Col>
    );
}


function NodeMenuItem(props) {
    return (
        <li className="NodeMenuItem"
            draggable={true}
            onDragStart={event => {
                event.dataTransfer.setData(
                    'storm-diagram-node',
                    JSON.stringify(props));
            }}
            style={{ color: props.nodeInfo.color }}>
            {props.nodeInfo.name}
        </li>
    )
}
