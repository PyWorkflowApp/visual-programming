import React, { useRef, useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import propTypes from 'prop-types';
import * as _ from 'lodash';
import * as API from "../../API";

export default class NodeConfig extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            disabled: false,
            data: {}
        };
        this.updateData = this.updateData.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    // callback to update form data in state;
    // resulting state will be sent to node config callback
    updateData(key, value) {
        this.setState((prevState) => ({
                ...prevState,
                data: {
                    ...prevState.data,
                    [key]: value
                }
            })
        );
    };

    // confirm, fire delete callback, close modal
    handleDelete() {
        if (window.confirm("Are you sure you want to delete this node?")) {
            this.props.onDelete();
            this.props.toggleShow();
        }
    };

    // collect config data, fire submit callback, close modal
    handleSubmit(e) {
        e.preventDefault();
        console.log(this.state.data);
        this.props.onSubmit(this.state.data);
        this.props.toggleShow();
    };

    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
                <Form onSubmit={this.handleSubmit}>
                    <Modal.Header>
                        <Modal.Title><b>{this.props.node.options.name}</b> Configuration</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {_.map(this.props.node.configParams, (info, key) =>
                            <OptionInput key={key} {...info} keyName={key}
                                         onChange={this.updateData}
                                         node={this.props.node}
                                         value={this.props.node.config[key]}
                                         disableFunc={(v) => this.setState({disabled: v})}/>
                        )}
                        <Form.Group>
                            <Form.Label>Node Description</Form.Label>
                            <Form.Control as="textarea" rows="2"
                                          name="description"
                                          defaultValue={this.props.node.config.description}/>
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="success" disabled={this.props.disabled} type="submit">Save</Button>
                        <Button variant="secondary" onClick={this.props.toggleShow}>Cancel</Button>
                        <Button variant="danger" onClick={this.handleDelete}>Delete</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        );
    }
}


NodeConfig.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
    onDelete: propTypes.func,
    onSubmit: propTypes.func
};


function OptionInput(props) {

    let inputComp;
    if (props.type === "file") {
        inputComp = <FileUpload disableFunc={props.disableFunc}
                        node={props.node}
                        name={props.keyName}
                        value={props.value} />
    } else if (props.type === "string") {
        inputComp = <Form.Control type="text" name={props.keyName}
                        defaultValue={props.value} />;
    } else if (props.type === "integer") {
        inputComp = <Form.Control type="number" name={props.keyName}
                                  defaultValue={props.value} />;
    } else {
        return (<></>)
    }
    return (
        <Form.Group>
                <Form.Label>{props.label}</Form.Label>
                <div style={{fontSize: '0.7rem'}}>{props.docstring}</div>
                { inputComp }
        </Form.Group>
    )
}


function FileUpload(props) {

    const input = useRef(null);
    const [fileName, setFileName] = useState(props.value || "");
    const [status, setStatus] = useState(props.value ? "ready" : "unconfigured");

    const uploadFile = async file => {
        props.disableFunc(true);
        setStatus("loading");
        const fd = new FormData();
        fd.append("file", file);
        fd.append("nodeId", props.node.options.id);
        API.uploadDataFile(fd)
            .then(resp => {
                setFileName(resp.filename);
                setStatus("ready");
                props.disableFunc(false);
                setStatus("ready");
            }).catch(() => {
                setStatus("failed");
            });
        input.current.value = null;
    };
    const onFileSelect = e => {
        e.preventDefault();
        if (!input.current.files) return;
        uploadFile(input.current.files[0]);
    };

    if (status === "loading") return (<div>Uploading file...</div>);
    const btnText = status === "ready" ? "Choose Different File" : "Choose File";
    let content;
    if (status === "ready") {
        const rxp = new RegExp(props.node.options.id + '-');
        content = (
            <div>
                <b style={{color: 'green'}}>File loaded:</b>&nbsp;
                {fileName.replace(rxp, '')}
            </div>
        )
    } else if (status === "failed") {
        content = (<div>Upload failed. Try a new file.</div>);
    }
    return (
        <>
            <input type="file" ref={input} onChange={onFileSelect}
                   style={{display: "none"}} />
            <input type="hidden" name={props.name} value={fileName} />
            <Button size="sm" onClick={() => input.current.click()}>{btnText}</Button>
            {content}
        </>
    )
}

