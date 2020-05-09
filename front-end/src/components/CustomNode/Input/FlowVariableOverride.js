import React, { useRef, useState, useEffect } from 'react';
import { Col, Button, Form } from 'react-bootstrap';

export default function FlowVariableOverride(props) {

    const handleSelect = (event) => {
        const uuid = event.target.value;
        const flow = props.flowNodes.find(d => d.node_id === uuid);
        const obj = {
            node_id: uuid,
            is_global: flow.is_global
        };
        props.onChange(obj);
    };
    const handleCheck = (event) => { props.onFlowCheck(event.target.checked) };

    return  (
        <Col>
            <Form.Check type="checkbox" inline
                        label="Use Flow Variable"
                        checked={props.checked} onChange={handleCheck} />
            {props.checked ?
                <Form.Control as="select" name={props.keyName} onChange={handleSelect}
                              value={props.flowValue.node_id}>
                    <option/>
                    {props.flowNodes.map(fv =>
                        <option  key={fv.node_id} value={fv.node_id}>
                            {fv.options ? fv.options.var_name : fv.option_values.var_name}
                        </option>
                    )}
                </Form.Control>
                : null
            }
        </Col>
    )
}
