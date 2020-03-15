import * as React from 'react';
import { PortWidget } from '@projectstorm/react-diagrams';
import '../../styles/CustomNode.css';


export class CustomNodeWidget extends React.Component {
    render() {
        return (
            <div className="custom-node" style={{ borderColor: this.props.node.color }}>
                <PortWidget engine={this.props.engine} port={this.props.node.getPort('in')}>
                    <div className="circle-port" />
                </PortWidget>
                <PortWidget engine={this.props.engine} port={this.props.node.getPort('out')}>
                    <div className="circle-port" />
                </PortWidget>
                <div className="custom-node-name">{this.props.node.options.type}</div>
            </div>
        );
    }
}
