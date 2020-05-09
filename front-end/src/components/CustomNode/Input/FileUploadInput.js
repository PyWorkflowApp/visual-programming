import React, { useRef, useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import * as API from '../../../API';

/**
 *  Component representing a file parameter.
 *  Uploads selected file to server upon selection, and passes
 *  the filename from the server response to the form callback.
 */
export default function FileUploadInput(props) {

    const input = useRef(null);
    const [fileName, setFileName] = useState(props.value || "");
    const [status, setStatus] = useState(props.value ? "ready" : "unconfigured");

    const {keyName, onChange} = props;
    // fire callback on mount to update node config state
    useEffect(() => {
            onChange(keyName, fileName);
        },
        [fileName, keyName, onChange]);

    const uploadFile = async file => {
        props.disableFunc(true);
        setStatus("loading");
        const fd = new FormData();
        fd.append("file", file);
        fd.append("nodeId", props.node.options.id);
        API.uploadDataFile(fd)
            .then(resp => {
                setFileName(resp.filename);
                setStatus("ready");
                props.disableFunc(false);
                setStatus("ready");
            }).catch(() => {
                setStatus("failed");
            });
        input.current.value = null;
    };
    const onFileSelect = e => {
        e.preventDefault();
        if (!input.current.files) {
          return;
        }
        
        uploadFile(input.current.files[0]);
    };

    if (status === "loading") return (<div>Uploading file...</div>);
    const btnText = status === "ready" ? "Choose Different File" : "Choose File";
    let content;
    if (status === "ready") {
        const rxp = new RegExp(props.node.options.id + '-');
        content = (
            <div>
                <b style={{color: 'green'}}>File loaded:</b>&nbsp;
                {fileName.replace(rxp, '')}
            </div>
        )
    } else if (status === "failed") {
        content = (<div>Upload failed. Try a new file.</div>);
    }
    return (
        <>
            <input type="file" ref={input} onChange={onFileSelect}
                   style={{display: "none"}} />
            <input type="hidden" name={props.name} value={fileName} />
            <Button size="sm" onClick={() => input.current.click()}>{btnText}</Button>
            {content}
        </>
    )
}
