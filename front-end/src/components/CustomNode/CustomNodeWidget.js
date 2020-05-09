import React from 'react';
import * as _ from 'lodash';
import { PortWidget } from '@projectstorm/react-diagrams';
import StatusLight from '../StatusLight';
import GraphView from './GraphView';
import NodeConfig from './NodeConfig';
import '../../styles/CustomNode.css';
import * as API from '../../API';

export default class CustomNodeWidget extends React.Component {

    constructor(props) {
        super(props);
        this.state = {showConfig: false, showGraph: false};
        this.icon = '9881';
    }

    componentDidMount() {
      this.toggleConfig = this.toggleConfig.bind(this);
      this.toggleGraph = this.toggleGraph.bind(this);
      this.handleDelete = this.handleDelete.bind(this);
      this.acceptConfiguration = this.acceptConfiguration.bind(this);
    }

    // show/hide node configuration modal
    toggleConfig = () =>  {
        this.setState({showConfig: !this.state.showConfig});
    }

    // show/hide node graph modal
    toggleGraph = () =>  {
      this.setState({showGraph: !this.state.showGraph});
    }

    // delete node from diagram model and redraw diagram
    handleDelete = () =>  {
        API.deleteNode(this.props.node).then(() => {
            this.props.node.remove();
            this.props.engine.repaintCanvas();
        }).catch(err => console.log(err));
    }

    acceptConfiguration(optionsData, flowData) {
        API.updateNode(this.props.node, optionsData, flowData).then(() => {
            this.props.node.setStatus("configured");
            this.forceUpdate();
            console.log("Node updated");
            this.props.engine.repaintCanvas();
        }).catch(err => console.log(err));
    }

    render() {
        const engine = this.props.engine;
        const allPorts = _.values(this.props.node.getPorts());
        const ports = allPorts.filter(p => !p.options.name.includes("flow"));
        const flowInPort = allPorts.find(p => p.options.name === "flow-in");
        const flowOutPort = allPorts.find(p => p.options.name === "flow-out");
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

        const flowPortWidgets = [flowInPort, flowOutPort].filter(p => p).map(port =>
            <PortWidget engine={engine} port={port} key={port.getID()}
                        className={`flow-port-div flow-port-div-${port.options.in ? "in" : "out"}`}>
                <div className="flow-port" />
            </PortWidget>
        );


        let graphView;
        let width = 40;
        if (this.props.node.options.node_type !== "flow_control") {
            graphView = (
                <div className="custom-node-tabular" onClick={this.toggleGraph}>
                  <img src="tabular-icon.png" alt="Tabular" style={{width:25, height:25}}/>
                </div>
            );
            width = 80;
        }

        return (
            <div className="custom-node-wrapper">
                <div className="custom-node-name">{this.props.node.options.name}</div>
                <div className="custom-node" style={{ borderColor: this.props.node.options.color, width: width }}>
                    <div className="custom-node-icons">
                        <div className="custom-node-configure" onClick={this.toggleConfig}>
                            {String.fromCharCode(this.icon)}
                        </div>
                        <NodeConfig node={this.props.node}
                            show={this.state.showConfig}
                            toggleShow={this.toggleConfig}
                            onDelete={this.handleDelete}
                            onSubmit={this.acceptConfiguration} />
                        {graphView}
                        <GraphView node={this.props.node}
                            show={this.state.showGraph}
                            toggleShow={this.toggleGraph}
                            onDelete={this.handleDelete}
                            onSubmit={this.acceptConfiguration} />
                    </div>
                    {flowPortWidgets}
                    <div className="port-col port-col-in">
                        { portWidgets["in"] }
                    </div>
                    <div className="port-col port-col-out">
                        { portWidgets["out"] }
                    </div>
                </div>
                <StatusLight status={this.props.node.options.status} />
                <div className="custom-node-description">{this.props.node.config.description}</div>
            </div>
        );
    }
}
