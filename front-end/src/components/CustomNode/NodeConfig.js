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
        if (!this.props.node) return null;
        return (
            <Modal show={this.props.show} onHide={this.props.toggleShow} centered
                onWheel={e => e.stopPropagation()}>
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
                                          onChange={e => this.updateData("description", e.target.value)}
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


/**
 *  Wrapper component to render form groups in the node config form.
 */
function OptionInput(props) {

    let inputComp;
    if (props.type === "file") {
        inputComp = <FileUploadInput {...props} />
    } else if (props.type === "string") {
        inputComp = <SimpleInput {...props} type="text" />
    } else if (props.type === "text") {
        inputComp = <SimpleInput {...props} type="textarea"/>
    } else if (props.type === "int") {
        inputComp = <SimpleInput {...props} type="number" />
    } else if (props.type === "boolean") {
        inputComp = <BooleanInput {...props} />
    } else if (props.type === "select") {
        inputComp = <SelectInput {...props} />
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


/**
 *  Component representing a file parameter.
 *  Uploads selected file to server upon selection, and passes
 *  the filename from the server response to the form callback.
 */
function FileUploadInput(props) {

    const input = useRef(null);
    const [fileName, setFileName] = useState(props.value || "");
    const [status, setStatus] = useState(props.value ? "ready" : "unconfigured");

    const {keyName, onChange} = props;
    // fire callback on mount to update node config state
    useEffect(() => {
            onChange(keyName, fileName);
        },
        [fileName, keyName, onChange]);

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

function SimpleInput(props) {

    const [value, setValue] = useState(props.value);
    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const {keyName, onChange, type} = props;
    // whenever value changes, fire callback to update config form
    useEffect(() => {
            const formValue = type === "number" ? Number(value) : value;
            onChange(keyName, formValue);
        },
        [value, keyName, onChange, type]);

    if (props.type === "textarea") {
        return (
            <Form.Control as="textarea" rows="7" name={props.keyName}
                              defaultValue={props.value}
                              onChange={handleChange} />
        )

    } else {
        return  (
            <Form.Control type={props.type} name={props.keyName}
                              defaultValue={props.value}
                              onChange={handleChange} />
        )
    }
}


function BooleanInput(props) {

    const [value, setValue] = useState(props.value);
    const handleChange = (event) => {
        setValue(event.target.checked);
    };

    const {keyName, onChange} = props;
    // whenever value changes, fire callback to update config form
    useEffect(() => {
            onChange(keyName, value);
        },
        [value, keyName, onChange]);

    return  (
        <Form.Check type="checkbox" name={props.keyName}
                      checked={value}
                      onChange={handleChange} />
    )
}


function SelectInput(props) {

    const [value, setValue] = useState(props.value);
    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const {keyName, onChange} = props;
    // whenever value changes, fire callback to update config form
    useEffect(() => {
            onChange(keyName, value);
        },
        [value, keyName, onChange]);

    return  (
        <Form.Control as="select" name={props.keyName}
                    value={value}
                    onChange={handleChange}>
            {props.options.map(opt =>
                <option key={opt} value={opt}>{opt}</option>
            )}
        </Form.Control>
    )
}
