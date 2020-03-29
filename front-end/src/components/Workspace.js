import React from 'react';
import * as _ from 'lodash';
import { Row, Col } from 'react-bootstrap';
import createEngine, { DiagramModel } from '@projectstorm/react-diagrams';
import { CanvasWidget } from '@projectstorm/react-canvas-core';
import { VPLinkFactory } from './VPLink/VPLinkFactory';
import { CustomNodeModel } from './CustomNode/CustomNodeModel';
import { CustomNodeFactory } from './CustomNode/CustomNodeFactory';
import '../styles/Workspace.css';

class Workspace extends React.Component {

    constructor(props) {
        super(props);
        this.engine = createEngine();
        this.engine.getNodeFactories().registerFactory(new CustomNodeFactory());
        this.engine.getLinkFactories().registerFactory(new VPLinkFactory());
        this.model = new DiagramModel();
        this.engine.setModel(this.model);
        this.engine.setMaxNumberPointsPerLink(0);
        this.state = {nodes: []};
    }

    componentDidMount() {
        async function getNodes() {
            const resp = await fetch("/workflow/nodes");
            return resp.json();
        }
        getNodes().then(nodes => this.setState({nodes: nodes}));
    }

    render() {
        // construct menu from JSON of node types
        const menu = _.map(this.state.nodes, (items, section) =>
            <div key={`node-menu-${section}`}>
                <b>{section}</b>
                <ul>
                { _.map(items, item => <NodeMenuItem {...item} />) }
                </ul>
            </div>
        );

        return (
            <Row className="Workspace">
                <Col xs={3} className="node-menu">
                    <div>Drag-and-drop nodes to build a workflow.</div>
                    <hr />
                    { menu }
                </Col>
                <Col xs={9}>
                    <div style={{position: 'relative', flexGrow: 1}}
                        onDrop={event => {
                            var data = JSON.parse(event.dataTransfer.getData('storm-diagram-node'));
                            var node = new CustomNodeModel(data);
                            var point = this.engine.getRelativeMousePoint(event);
                            node.setPosition(point);
                            this.model.addNode(node);
                            this.forceUpdate();
                        }}
                    onDragOver={event => {
                            event.preventDefault();
                    }}
                    >
                        <CanvasWidget className="diagram-canvas" engine={this.engine} />
                    </div>
                </Col>
            </Row>
        );
    }
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
            style={{ color: props.color }}>
            {props.name}
        </li>
    )
}

export default Workspace;
