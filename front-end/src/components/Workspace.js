import React, { useRef } from 'react';
import { Row, Col, Button } from 'react-bootstrap';
import createEngine, { DiagramModel } from '@projectstorm/react-diagrams';
import { CanvasWidget } from '@projectstorm/react-canvas-core';
import { VPLinkFactory } from './VPLink/VPLinkFactory';
import { CustomNodeModel } from './CustomNode/CustomNodeModel';
import { CustomNodeFactory } from './CustomNode/CustomNodeFactory';
import { VPPortFactory } from './VPPort/VPPortFactory';
import * as API from '../API';
import NodeMenu from './NodeMenu';
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
        this.load = this.load.bind(this);
        this.clear = this.clear.bind(this);
        this.handleNodeCreation = this.handleNodeCreation.bind(this);
    }

    componentDidMount() {
        API.getNodes()
            .then(nodes => this.setState({nodes: nodes}))
            .catch(err => console.log(err));
        API.initWorkflow().catch(err => console.log(err));
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
     * Remove all nodes from diagram and initialize new workflow on server
     */
    clear() {
        if (window.confirm("Clear diagram? You will lose all work.")) {
            this.model.getNodes().forEach(n => n.remove());
            API.initWorkflow().catch(err => console.log(err));
            this.engine.repaintCanvas();
        }
    }

    // takes data from node drop and creates node on server and in diagram
    handleNodeCreation(event) {
        const data = JSON.parse(event.dataTransfer.getData('storm-diagram-node'));
        if (!data) return;
        const node = new CustomNodeModel(data.nodeInfo, data.config),
            point = this.engine.getRelativeMousePoint(event);
        node.setPosition(point);
        API.addNode(node).then(() => {
            this.model.addNode(node);
            this.forceUpdate();
        }).catch(err => console.log(err));
    }

    render() {
        return (
            <>
                <Row className="mb-3">
                    <Col md={12}>
                        <Button size="sm" onClick={() => API.save(this.model.serialize())}>
                            Save
                        </Button>{' '}
                        <FileUpload handleData={this.load}/>{' '}
                        <Button size="sm" onClick={this.clear}>Clear</Button>
                    </Col>
                </Row>
                <Row className="Workspace">
                    <NodeMenu nodes={this.state.nodes} />
                    <Col xs={10}>
                        <div style={{position: 'relative', flexGrow: 1}}
                            onDrop={event => this.handleNodeCreation(event)}
                            onDragOver={event => event.preventDefault() }>
                            <CanvasWidget className="diagram-canvas" engine={this.engine} />
                        </div>
                    </Col>
                </Row>
            </>
        );
    }
}


function FileUpload(props) {
    const input = useRef(null);
    const uploadFile = file => {
        const form = new FormData();
        form.append("file", file);
        API.uploadWorkflow(form).then(json => {
            props.handleData(json.react);
        }).catch(err => {
            console.log(err);
        });
        input.current.value = null;
    };
    const onFileSelect = e => {
        e.preventDefault();
        if (!input.current.files) return;
        uploadFile(input.current.files[0]);
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
