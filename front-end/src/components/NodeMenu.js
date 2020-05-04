import React from 'react';
import * as _ from 'lodash';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import CustomNodeUpload from "./CustomNodeUpload";


export default function NodeMenu(props) {
    // construct menu from JSON of node types
    return (
        <div className="NodeMenu">
            <h3>Node Menu</h3>
            <div>Drag-and-drop nodes to build a workflow.</div>
            <hr />
            {_.map(props.nodes, (items, section) =>
                <div key={`node-menu-${section}`}>
                    <span className="node-section-title">{section}</span>
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
       </div>
    );
}


/**
 * Format docstring with newlines into tooltip content
 * @param string - node docstring
 * @returns {array} - array of strings and HTML elements
 */
function formatTooltip(string) {
    const split = string.split("\n");
    const out = [];
    split.forEach((line, i) => {
        out.push(line);
        out.push(<br  key={i} />);
    });
    out.pop();
    return out;
}


function NodeMenuItem(props) {
    if (!props.nodeInfo.missing_packages) {
        const tooltip = props.nodeInfo.doc ? formatTooltip(props.nodeInfo.doc) : "This node has no documentation."
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
        let tooltip = "These Python modules could not be imported:\n\n"
            + props.nodeInfo.missing_packages.join("\n");
        tooltip = formatTooltip(tooltip);
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
        <Tooltip {...props} ref={ref}>
            <div style={{textAlign: "left"}}>
                {props.message}
            </div>
        </Tooltip>
    )
});

