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
            const resp = await fetch("/nodes");
            return resp.json();
        }
        async function startWorkflow() {
            const resp = await fetch("/workflow/new");
            return resp.json();
        }
        getNodes().then(nodes => this.setState({nodes: nodes}));
        startWorkflow().then(resp => console.log(resp));
    }

    /**
     * serialize model, POST to server, download response as JSON file
     */
    async save() {
        const data = JSON.stringify(this.model.serialize());
        const resp = await fetch("/workflow/save", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: data
        });
        if (resp.status !== 200) {
            console.log(await resp.json());
        } else {
            const downloadData = await resp.json();
            const dataStr = "data:text/json;charset=utf-8,"
                + encodeURIComponent(JSON.stringify(downloadData));
            const anchor = document.createElement("a")
            anchor.href = dataStr;
            anchor.download = downloadData.filename || "diagram.json";
            anchor.click();
            anchor.remove();
        }
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

    async handleNodeCreation(event) {
        const data = JSON.parse(event.dataTransfer.getData('storm-diagram-node'));
        if (!data) return;
        const config = data.options;
        delete data.options;
        const node = new CustomNodeModel(data, config),
            point = this.engine.getRelativeMousePoint(event);
        node.setPosition(point);
        data.node_id = node.options.id;
        const resp = await fetch("/node/", {
            method: "POST",
            body: JSON.stringify(data)
        });
        if (resp.status === 200) {
            this.model.addNode(node);
            this.forceUpdate();
            console.log(await resp.json());
        } else {
            console.log("Failed to create node on back end.")
        }
    }

    render() {
        // construct menu from JSON of node types
        const menu = _.map(this.state.nodes, (items, section) =>
            <div key={`node-menu-${section}`}>
                <b>{section}</b>
                <ul>
                { _.map(items, item => <NodeMenuItem {...item} key={item.node_key} />) }
                </ul>
            </div>
        );

        return (
            <>
                <Row className="mb-3">
                    <Col md={12}>
                        <Button size="sm" onClick={this.save}>Save</Button>{' '}
                        <FileUpload handleData={this.load}/>{' '}
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
    const uploadFile = async file => {
        const form = new FormData();
        form.append("file", file);
        const resp = await fetch("/workflow/open", {
            method: "POST",
            body: form
        });
        if (resp.status !== 200) {
            console.log("Failed to open workflow.");
        } else {
            const respData = await resp.json();
            props.handleData(respData.react);
        }
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
