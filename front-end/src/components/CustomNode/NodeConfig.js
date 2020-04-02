import React, { useRef } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import propTypes from 'prop-types';
import * as _ from 'lodash';

function NodeConfig(props) {

    const form = useRef();

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
                                value={props.node.config[key]} />
                        )}
                        <Form.Group>
                            <Form.Label>Node Description</Form.Label>
                            <Form.Control as="textarea" rows="2"
                                name="description"
                                defaultValue={props.node.config.description} />
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="success" type="submit">Save</Button>
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
}


function OptionInput(props) {
    let inputComp;
    if (props.type === "file") {
        inputComp = <input type="file" name={props.keyName} />;
    } else if (props.type === "string") {
        inputComp = <Form.Control type="text" name={props.keyName}
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

export default NodeConfig;
