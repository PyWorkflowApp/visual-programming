import React from 'react';
import * as _ from 'lodash';
import { Col } from 'react-bootstrap';
import CustomNodeUpload from "./CustomNodeUpload";


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
                            const data = {...item}; // copy so we can mutate
                            const config = data.options;
                            delete data.options;
                            return (
                                <NodeMenuItem key={data.node_key} nodeInfo={data} config={config} />
                            )}
                        )}
                    </ul>
                </div>
            )}
            <CustomNodeUpload onUpload={props.onUpload} />
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
