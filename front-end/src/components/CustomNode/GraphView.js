import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';

function GraphView(props) {

    const onClose = () => {
        props.toggleShow();
    };


    return (
            <Modal show={props.show} onHide={props.toggleShow} centered>
            <Modal.Header>
                <Modal.Title><b>{props.node.options.name}</b> View</Modal.Title>
            </Modal.Header>
            <Modal.Body>

            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onClose}>Accept</Button>
            </Modal.Footer>
            </Modal>
    );
}


GraphView.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
    onClose: propTypes.func,
}

export default GraphView;
