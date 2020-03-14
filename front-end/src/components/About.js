import React, { useState } from 'react';
import { Modal } from 'react-bootstrap';

function About(props) {
    const [show, setShow] = useState(props.show);
    const [info, setInfo] = useState();

    async function fetchInfo() {
        const resp = await fetch("/info");
        const data = await resp.json();
        setInfo(data);
    }

    const handleClose = () => setShow(false);
    const handleShow = (e) => {
        e.preventDefault();
        fetchInfo()
        setShow(true);
    }

    return (
        <>
            <div><span className="btn btn-link" onClick={handleShow}>About</span></div>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title><b>About Visual Programming</b></Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {JSON.stringify(info)}
                </Modal.Body>
            </Modal>
        </>
    );
}

export default About;
