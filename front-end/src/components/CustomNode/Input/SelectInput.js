import React, { useRef, useState, useEffect } from 'react';
import { Form } from 'react-bootstrap';

export default function SelectInput(props) {

    const [value, setValue] = useState(props.value);
    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const {keyName, onChange} = props;
    // whenever value changes, fire callback to update config form
    useEffect(() => {
            onChange(keyName, value);
        },
        [value, keyName, onChange]);

    return  (
        <Form.Control as="select" name={props.keyName}
                    value={value}
                    onChange={handleChange}>
            {props.options.map(opt =>
                <option key={opt} value={opt}>{opt}</option>
            )}
        </Form.Control>
    )
}
