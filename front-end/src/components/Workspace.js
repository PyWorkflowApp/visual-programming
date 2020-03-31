import React, { useRef } from 'react';
import * as _ from 'lodash';
import { Row, Col, Button } from 'react-bootstrap';
import createEngine, { DiagramModel } from '@projectstorm/react-diagrams';
import { CanvasWidget } from '@projectstorm/react-canvas-core';
import { VPLinkFactory } from './VPLink/VPLinkFactory';
import { CustomNodeModel } from './CustomNode/CustomNodeModel';
import { CustomNodeFactory } from './CustomNode/CustomNodeFactory';
import { VPPortFactory } from './VPPort/VPPortFactory';
import '../styles/Workspace.css';

class Workspace extends React.Component {

    constructor(props) {
        super(props);
        this.engine = createEngine();
        this.engine.getNodeFactories().registerFactory(new CustomNodeFactory());
        this.engine.getLinkFactories().registerFactory(new VPLinkFactory());
        this.engine.getPortFactories().registerFactory(new VPPortFactory());
        this.model = new DiagramModel();
        this.engine.setModel(this.model);
        this.engine.setMaxNumberPointsPerLink(0);
        this.state = {nodes: []};
        this.save = this.save.bind(this);
        this.load = this.load.bind(this);
        this.clear = this.clear.bind(this);
    }

    componentDidMount() {
        async function getNodes() {
            const resp = await fetch("/workflow/nodes");
            return resp.json();
        }
        getNodes().then(nodes => this.setState({nodes: nodes}));
    }

    /**
     * serialize model and download as JSON file
     */
    save() {
        const data = JSON.stringify(this.model.serialize());
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(data)
        const anchor = document.createElement("a")
        anchor.href = dataStr;
        anchor.download = "diagram.json";
        anchor.click();
        anchor.remove();
    }

    /**
     * Load diagram JSON and render
     * @param diagramData: serialized diagram JSON
     */
    load(diagramData) {
        this.model.deserializeModel(diagramData, this.engine);
        // redraw is buggy if you don't wait a little bit
        setTimeout(() => this.engine.repaintCanvas(), 100);
    }

    /**
     * Remove all nodes from diagram
     */
    clear() {
        if (window.confirm("Clear diagram?")) {
            this.model.getNodes().forEach(n => n.remove());
            this.engine.repaintCanvas();
        }
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
            <>
                <Row className="mb-3">
                    <Col md={12}>
                        <Button size="sm" onClick={this.save}>Save</Button>{' '}
                        <FileUpload handleFile={this.load}/>{' '}
                        <Button size="sm" onClick={this.clear}>Clear</Button>
                    </Col>
                </Row>
                <Row className="Workspace">
                    <Col xs={2} className="node-menu">
                        <div>Drag-and-drop nodes to build a workflow.</div>
                        <hr />
                        { menu }
                    </Col>
                    <Col xs={10}>
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
            </>
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


function FileUpload(props) {
    const input = useRef(null);
    const readFile = file => {
        if (!file) return;
        const fr = new FileReader();
        fr.addEventListener("load", () => {
            const data = JSON.parse(fr.result);
            props.handleFile(data);
        });
        fr.readAsText(file);
    };
    const onFileSelect = e => {
        e.preventDefault();
        readFile(input.current.files[0]);
    };
    return (
        <>
        <input type="file" ref={input} onChange={onFileSelect}
            style={{display: "none"}} />
        <Button size="sm" onClick={() => input.current.click()}>Load</Button>
        </>
    )
}

export default Workspace;
