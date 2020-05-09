import React from "react";
import * as API from "../API";
import {Button} from "react-bootstrap";

export default class CustomNodeUpload extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          status: "ready",
          input: React.createRef()
        }

        this.onUpload = props.onUpload;
    }

    uploadFile = async file => {
      this.setState({status: "loading"});
        const fd = new FormData();
        fd.append("file", file);
        API.uploadDataFile(fd)
            .then(resp => {
                this.onUpload();
                this.setState({status: "ready"});
            }).catch(() => {
              this.setState({status: "failed"});
        });

        this.setState({input: React.createRef()});
    };

    onFileSelect = e => {
        e.preventDefault();
        if (!this.state.input.current || !this.state.input.current.files) {
          return;
        }

        this.uploadFile(this.state.input.current.files[0]);
    };

    render() {
      let content;
      if (this.state.status === "loading") {
          content = <div>Uploading file...</div>;
      } else if (this.state.status === "failed") {
          content = (<div>Upload failed. Try a new file.</div>);
      }
      return (
          <>
              <input type="file" ref={this.state.input} onChange={this.onFileSelect}
                     style={{display: "none"}} />
              <Button size="sm" onClick={() => this.state.input.current.click()}
                      variant="success"
                      disabled={this.state.status === "loading"}>
                  Add Custom Node
              </Button>
              {content}
          </>
      )
    }
}
