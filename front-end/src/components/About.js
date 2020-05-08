import React, { useState } from 'react';
import { Modal } from 'react-bootstrap';

export default class About extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
          show: props.show,
          info: {}};
    }

    componentDidMount() {

    }

    fetchInfo = async () => {
        const resp = await fetch("/info");
        const data = await resp.json();
        this.setState({info: data});
    }

    handleClose = () => {
      this.setState({show: false});
    }

    handleShow = (e) => {
        e.preventDefault();
        this.fetchInfo()
        this.setState({show: true});
    }

    render() {
      return (
          <>
              <div><span className="btn btn-link" onClick={this.handleShow}>About</span></div>

              <Modal show={this.state.show} onHide={this.handleClose}>
                  <Modal.Header closeButton>
                      <Modal.Title><b>About Visual Programming</b></Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                      {JSON.stringify(this.state.info)}
                  </Modal.Body>
              </Modal>
          </>
      );
    }
}
