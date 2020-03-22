import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import propTypes from 'prop-types';

function NodeConfig(props) {

    //TODO: going to need a much more flexible way of creating
    // the form fields and handling changes, rather than explicit
    // state variables and handlers

    const [description, setDescription] = useState();
    const handleDescriptionChange = (e) => {
        setDescription(e.target.value);
    }


    // confirm, fire delete callback, close modal
    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this node?")) {
            props.onDelete();
            props.toggleShow();
        }
    }

    // fire submit callback, close modal
    const handleSubmit = (e) => {
        e.preventDefault();
        props.onSubmit({description: description});
        props.toggleShow();
    }

    return (
            <Modal show={props.show} onHide={props.toggleShow} centered>
                <Form onSubmit={handleSubmit}>
                    <Modal.Header>
                        <Modal.Title><b>{props.node.options.name}</b> Configuration</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                            <Form.Label>Node Description</Form.Label>
                            <Form.Control as="textarea" rows="2" value={description}
                                onChange={handleDescriptionChange} />
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


export default NodeConfig;
