import React from 'react';
import * as _ from 'lodash';
import { Col, OverlayTrigger, Tooltip } from 'react-bootstrap';
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
                                <NodeMenuItem key={data.node_key || data.filename}
                                              nodeInfo={data} config={config} />
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
    if (!props.nodeInfo.missing_packages) {
        const tooltip = props.nodeInfo.doc || "This node has no documentation."
        return (
            <OverlayTrigger
                placement="right"
                delay={{ show: 250, hide: 250 }}
                overlay={<NodeTooltip message={tooltip} />}>
                <li className="NodeMenuItem"
                    draggable={true}
                    onDragStart={event => {
                        event.dataTransfer.setData(
                            'storm-diagram-node',
                            JSON.stringify(props));
                    }}
                    style={{color: props.nodeInfo.color}}>
                    {props.nodeInfo.name}
                </li>
            </OverlayTrigger>
        )
    } else {
        let tooltip = "These Python modules could not be imported: ";
        tooltip += props.nodeInfo.missing_packages.join(", ");
        return (
            <OverlayTrigger
                placement="right"
                delay={{ show: 250, hide: 250 }}
                overlay={<NodeTooltip message={tooltip} />}>
                <li className="NodeMenuItem invalid">{props.nodeInfo.filename}</li>
            </OverlayTrigger>
        )
    }
}


// Overlay with props has to use ref forwarding
const NodeTooltip = React.forwardRef((props, ref) => {
    return (
        <Tooltip {...props} ref={ref}>{props.message}</Tooltip>
    )
});

