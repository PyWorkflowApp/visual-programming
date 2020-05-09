import React, { useRef, useState, useEffect } from 'react';
import { Col, Modal, Button, Form } from 'react-bootstrap';
import propTypes from 'prop-types';
import * as _ from 'lodash';
import * as API from '../../API';
import '../../styles/NodeConfig.css';
import OptionInput from './Input/OptionInput'

export default class NodeConfig extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            disabled: false,
            data: {},
            flowData: {},
            flowNodes: []
        };
        this.updateData = this.updateData.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    getFlowNodes() {
        if (!this.props.node) return;
        API.getNode(this.props.node.options.id)
            .then(node => this.setState({flowNodes: node.flow_variables}))
            .catch(err => console.log(err));
    }

    componentDidUpdate(prevProps) {
        if (!prevProps.show && this.props.show) this.getFlowNodes();
    }

    // callback to update form data in state;
    // resulting state will be sent to node config callback
    updateData(key, value, flow = false) {
        if (flow) {
            this.setState((prevState) => ({
                    ...prevState,
                    flowData: {
                        ...prevState.flowData,
                        [key]: value
                    }
                })
            );
        } else {
            this.setState((prevState) => ({
                    ...prevState,
                    data: {
                        ...prevState.data,
                        [key]: value
                    }
                })
            );
        }
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
        // remove items from flow vars if null
        const flowData = {...this.state.flowData};
        for (let key in flowData) {
            if (flowData[key] === null) delete flowData[key];
        }
        this.props.onSubmit(this.state.data, flowData);
        this.props.toggleShow();
    };

    render() {
        if (!this.props.node) {
          return null;
        }

        return (
            <Modal show={this.props.show} onHide={this.props.toggleShow} centered
                   dialogClassName="NodeConfig"
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
                                         flowValue={this.props.node.options.option_replace ?
                                            this.props.node.options.option_replace[key] : null}
                                         flowNodes={this.state.flowNodes}
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
