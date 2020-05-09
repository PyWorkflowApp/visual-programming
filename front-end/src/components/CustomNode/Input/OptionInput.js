import React, { useState } from 'react';
import { Col, Form } from 'react-bootstrap';
import BooleanInput from './BooleanInput'
import FileUploadInput from './FileUploadInput'
import FlowVariableOverride from './FlowVariableOverride'
import SelectInput from './SelectInput'
import SimpleInput from './SimpleInput'


/**
 *  Wrapper component to render form groups in the node config form.
 */
export default function OptionInput(props) {

    const [isFlow, setIsFlow] = useState(props.flowValue ? true : false);

    const handleFlowCheck = (bool) => {
        // if un-checking, fire callback with null so no stale value is in `option_replace`
        if (!bool) props.onChange(props.keyName, null, true);
        setIsFlow(bool);
    };

    // fire callback to update `option_replace` with flow node info
    const handleFlowVariable = (value) => {
        props.onChange(props.keyName, value, true);
    };

    let inputComp;
    if (props.type === "file") {
        inputComp = <FileUploadInput {...props} disabled={isFlow} />
    } else if (props.type === "string") {
        inputComp = <SimpleInput {...props} type="text" disabled={isFlow} />
    } else if (props.type === "text") {
        inputComp = <SimpleInput {...props} type="textarea" disabled={isFlow} />
    } else if (props.type === "int") {
        inputComp = <SimpleInput {...props} type="number" disabled={isFlow} />
    } else if (props.type === "boolean") {
        inputComp = <BooleanInput {...props} disabled={isFlow} />
    } else if (props.type === "select") {
        inputComp = <SelectInput {...props} />
    } else {
        return (<></>)
    }

    const hideFlow = props.node.options.is_global
                        || props.type === "file" || props.flowNodes.length === 0;
    return (
        <Form.Group>
            <Form.Label>{props.label}</Form.Label>
            <div className="option-docstring">{props.docstring}</div>
            <Form.Row>
                <Col xs={hideFlow ? 12 : 8}>{ inputComp }</Col>
                {hideFlow ? null :
                    <FlowVariableOverride keyName={props.keyName}
                                          flowValue={props.flowValue || {}}
                                          flowNodes={props.flowNodes || []}
                                          checked={isFlow}
                                          onFlowCheck={handleFlowCheck}
                                          onChange={handleFlowVariable} />
                }
            </Form.Row>
        </Form.Group>
    )
}
