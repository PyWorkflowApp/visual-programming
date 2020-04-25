import React, {useRef, useState} from "react";
import * as API from "../API";
import {Button} from "react-bootstrap";


export default function CustomNodeUpload({ onUpload }) {

    const input = useRef(null);
    const [status, setStatus] = useState("ready");

    const uploadFile = async file => {
        setStatus("loading");
        const fd = new FormData();
        fd.append("file", file);
        API.uploadDataFile(fd)
            .then(resp => {
                onUpload();
                setStatus("ready");
            }).catch(() => {
                setStatus("failed");
        });
        input.current.value = null;
    };
    const onFileSelect = e => {
        e.preventDefault();
        if (!input.current.files) return;
        uploadFile(input.current.files[0]);
    };

    let content;
    if (status === "loading") {
        content = <div>Uploading file...</div>;
    } else if (status === "failed") {
        content = (<div>Upload failed. Try a new file.</div>);
    }
    return (
        <>
            <input type="file" ref={input} onChange={onFileSelect}
                   style={{display: "none"}} />
            <Button size="sm" onClick={() => input.current.click()}
                    variant="success"
                    disabled={status === "loading"}>
                Add Custom Node
            </Button>
            {content}
        </>
    )
}
