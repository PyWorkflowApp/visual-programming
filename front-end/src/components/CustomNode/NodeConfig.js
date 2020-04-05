import React, { useRef, useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import propTypes from 'prop-types';
import * as _ from 'lodash';
import * as API from "../../API";

export default function NodeConfig(props) {

    const form = useRef();
    const [disabled, setDisabled] = useState(false);

    // confirm, fire delete callback, close modal
    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this node?")) {
            props.onDelete();
            props.toggleShow();
        }
    };

    // collect config data, fire submit callback, close modal
    const handleSubmit = (e) => {
        e.preventDefault();
        const fd = new FormData(form.current);
        const data = {};
        fd.forEach((value, key) => {data[key] = value;});
        props.onSubmit(data);
        props.toggleShow();
    };

    return (
            <Modal show={props.show} onHide={props.toggleShow} centered>
                <Form onSubmit={handleSubmit} ref={form}>
                    <Modal.Header>
                        <Modal.Title><b>{props.node.options.name}</b> Configuration</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        { _.map(props.node.configParams, (info, key) =>
                            <OptionInput key={key} {...info} keyName={key}
                                node={props.node}
                                value={props.node.config[key]}
                                disableFunc={setDisabled}/>
                        )}
                        <Form.Group>
                            <Form.Label>Node Description</Form.Label>
                            <Form.Control as="textarea" rows="2"
                                name="description"
                                defaultValue={props.node.config.description} />
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="success" disabled={disabled} type="submit">Save</Button>
                        <Button variant="secondary" onClick={props.toggleShow}>Cancel</Button>
                        <Button variant="danger" onClick={handleDelete}>Delete</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
    );
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
                <Form.Label>{props.name}</Form.Label>
                <div style={{fontSize: '0.7rem'}}>{props.desc}</div>
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

