import React from 'react';
import { Button } from 'react-bootstrap';

export default class FileUpload extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      input: React.createRef()
    }
  }

   uploadFile = file => {
        const form = new FormData();
        form.append("file", file);
        API.uploadWorkflow(form).then(json => {
            this.props.handleData(json);
        }).catch(err => {
            console.log(err);
        });
        this.setState({input: React.createRef()});
    };

    onFileSelect = e => {
        e.preventDefault();
        if (!this.state.input.current || !this.state.input.current.files) {
          return;
        }

        uploadFile(this.state.input.current.files[0]);
    };

    render() {
      return (
          <>
          <input type="file" ref={this.state.input} onChange={this.onFileSelect}
              style={{display: "none"}} />
          <Button size="sm" onClick={() => this.state.input.current.click()}>Load</Button>
          </>
      )
    }
}
