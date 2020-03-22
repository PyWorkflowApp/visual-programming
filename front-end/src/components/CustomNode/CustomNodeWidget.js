import React from 'react';
import * as _ from 'lodash';
import { PortWidget } from '@projectstorm/react-diagrams';
import StatusLight from '../StatusLight';
import NodeConfig from './NodeConfig';
import '../../styles/CustomNode.css';


export class CustomNodeWidget extends React.Component {

    constructor(props) {
        super(props);
        this.state = {showConfig: false};
        this.toggleConfig = this.toggleConfig.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.acceptConfiguration = this.acceptConfiguration.bind(this);
    }

    // show/hide node configuration modal
    toggleConfig() {
        this.setState({showConfig: !this.state.showConfig});
    }

    // delete node from diagram model and redraw diagram
    handleDelete() {
        this.props.node.remove();
        this.props.engine.repaintCanvas();
    }

    acceptConfiguration(formData) {
        this.props.node.setDescription(formData.description);
        this.props.engine.repaintCanvas();
    }

    render() {
        const engine = this.props.engine;
        const ports = _.values(this.props.node.getPorts());
        // group ports by type (in/out)
        const sortedPorts = _.groupBy(ports, p => p.options.type);
        // create PortWidget array for each type
        const portWidgets = {};
        for (let portType in sortedPorts) {
            portWidgets[portType] = sortedPorts[portType].map(port =>
                <PortWidget engine={engine} port={port} key={port.getID()}>
                        <div className="triangle-port" />
                </PortWidget>
            );
        }
        return (
            <div className="custom-node-wrapper">
                <div className="custom-node-name">{this.props.node.options.name}</div>
                <div className="custom-node" style={{ borderColor: this.props.node.color }}>
                    <div className="custom-node-configure" onClick={this.toggleConfig}>&#x2699;</div>
                    <NodeConfig node={this.props.node}
                        show={this.state.showConfig}
                        toggleShow={this.toggleConfig}
                        onDelete={this.handleDelete}
                        onSubmit={this.acceptConfiguration} />
                    <div className="port-col port-col-in">
                        { portWidgets["in"] }
                    </div>
                    <div className="port-col port-col-out">
                        { portWidgets["out"] }
                    </div>
                </div>
                <StatusLight status="unconfigured" />
                <div className="custom-node-description">{this.props.node.getDescription()}</div>
            </div>
        );
    }
}
