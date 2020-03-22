import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';

function NodeConfig(props) {

    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this node?")) {
            props.handleDelete();
            props.toggleShow();
        }
    }

    return (
            <Modal show={props.show} onHide={props.toggleShow} centered>
                <Modal.Header>
                    <Modal.Title><b>{props.node.options.name}</b> Configuration</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="success" onClick={props.toggleShow}>Save</Button>
                    <Button variant="secondary" onClick={props.toggleShow}>Cancel</Button>
                    <Button variant="danger" onClick={handleDelete}>Delete</Button>
                </Modal.Footer>
            </Modal>
    );
}


NodeConfig.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
}

export default NodeConfig;
