import React from 'react';
import * as _ from 'lodash';
import { PortWidget } from '@projectstorm/react-diagrams';
import StatusLight from '../StatusLight';
import GraphView from './GraphView';
import NodeConfig from './NodeConfig';
import '../../styles/CustomNode.css';

export class CustomNodeWidget extends React.Component {

    constructor(props) {
        super(props);
        this.state = {showConfig: false, showGraph: false};
        this.toggleConfig = this.toggleConfig.bind(this);
        this.toggleGraph = this.toggleGraph.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.acceptConfiguration = this.acceptConfiguration.bind(this);
        this.icon = '9881';
    }

    // show/hide node configuration modal
    toggleConfig() {
        this.setState({showConfig: !this.state.showConfig});
    }

    // show/hide node graph modal
    toggleGraph() {
      this.setState({showGraph: !this.state.showGraph});
    }

    // delete node from diagram model and redraw diagram
    async handleDelete() {
        const id = this.props.node.options.id;
        const resp = await fetch(`/node/${id}`, {
            method: "DELETE"
        });
        if (resp.status !== 200) {
            console.log("Failed to delete node on back end.")
        } else {
            this.props.node.remove();
            this.props.engine.repaintCanvas();
            console.log(await resp.json());
        }
    }

    async acceptConfiguration(formData) {
        this.props.node.config = formData;
        console.log(formData);
        const node = this.props.node;
        const payload = {...node.options, options: node.config};
        const resp = await fetch(`/node/${node.options.id}`, {
            method: "POST",
            body: JSON.stringify(payload)
        });
        if (resp.status !== 200) {
            console.log("Failed to update node on back end.")
        } else {
            console.log(await resp.json());
            this.forceUpdate();
            this.props.engine.repaintCanvas();
        }
    }

    render() {
        const engine = this.props.engine;
        const ports = _.values(this.props.node.getPorts());
        // group ports by type (in/out)
        const sortedPorts = _.groupBy(ports, p => p.options.in === true ? "in" : "out");
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
                <div className="custom-node" style={{ borderColor: this.props.node.options.color }}>
                    <div className="custom-node-configure" onClick={this.toggleConfig}>{String.fromCharCode(this.icon)}</div>
                    <NodeConfig node={this.props.node}
                        show={this.state.showConfig}
                        toggleShow={this.toggleConfig}
                        onDelete={this.handleDelete}
                        onSubmit={this.acceptConfiguration} />
                    <div className="custom-node-tabular"  onClick={this.toggleGraph}>
                      <img src="tabular-icon.png" alt="Tabular" style={{width:25, height:25}}></img>
                    </div>
                    <GraphView node={this.props.node}
                        show={this.state.showGraph}
                        toggleShow={this.toggleGraph}
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
                <div className="custom-node-description">{this.props.node.config.description}</div>
            </div>
        );
    }
}
