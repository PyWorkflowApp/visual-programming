import * as React from 'react';
import * as _ from 'lodash';
import { PortWidget } from '@projectstorm/react-diagrams';
import '../../styles/CustomNode.css';


export class CustomNodeWidget extends React.Component {

    render() {
        const engine = this.props.engine;
        const ports = _.values(this.props.node.getPorts());
        // group ports by type (in/out)
        const sortedPorts = _.groupBy(ports, p => p.options.type);
        // create PortWidget array for each type
        const portWidgets = {};
        for (let portType in sortedPorts) {
            portWidgets[portType] = sortedPorts[portType].map(port =>
                <PortWidget engine={engine} port={port}>
                        <div className="triangle-port" />
                </PortWidget>
            );
        }
        return (
            <div className="custom-node-wrapper">
                <div className="custom-node-name">{this.props.node.options.name}</div>
                <div className="custom-node" style={{ borderColor: this.props.node.color }}>
                    <div className="port-col port-col-in">
                        { portWidgets["in"] }
                    </div>
                    <div className="port-col port-col-out">
                        { portWidgets["out"] }
                    </div>
                </div>
            </div>
        );
    }
}
