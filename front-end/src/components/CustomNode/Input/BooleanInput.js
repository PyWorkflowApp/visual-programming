import React, { useRef, useState, useEffect } from 'react';
import { Form } from 'react-bootstrap';

export default function BooleanInput(props) {

    const [value, setValue] = useState(props.value);
    const handleChange = (event) => {
        setValue(event.target.checked);
    };

    const {keyName, onChange} = props;
    // whenever value changes, fire callback to update config form
    useEffect(() => {
            onChange(keyName, value);
        },
        [value, keyName, onChange]);

    return  (
        <Form.Check type="checkbox" name={props.keyName}
                    disabled={props.disabled}
                    checked={value}
                    onChange={handleChange} />
    )
}
