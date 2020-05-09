import React, { useRef, useState, useEffect } from 'react';
import { Form } from 'react-bootstrap';

export default function SimpleInput(props) {

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

    const extraProps = props.type === "textarea"
        ? {as: "textarea", rows: props.rows || 7}
        : {type: props.type};
    return (
        <Form.Control {...extraProps} name={props.keyName}
                      disabled={props.disabled}
                      defaultValue={props.value}
                      onChange={handleChange} />
    )
}
