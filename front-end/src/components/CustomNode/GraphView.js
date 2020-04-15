import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';
import { VariableSizeGrid as Grid } from 'react-window';
import * as API from "../../API";

export default class GraphView extends React.Component {

    constructor(props) {
      super(props);
      this.key_id = props.node.getNodeId();
      this.columnCount = 0;
      this.rowCount = 0;
      this.state = { data: [] };
    }

    load = () => {
          console.log("Loading data");
          const jsonResponse = API.retrieveData(this.key_id)
          console.log("response type: " jsonResponse)
          this.setState({ data: jsonResponse });
    }

    onClose = () => {
        this.props.toggleShow();
    };

    columnWidths = new Array(this.columnCount)
      .fill(true)
      .map(() => 75 + Math.round(Math.random() * 50));

    rowHeights = new Array(this.rowCount)
      .fill(true)
      .map(() => 25 + Math.round(Math.random() * 50));

    Cell = ({ columnIndex, rowIndex, style }) => (
      <div style={style}>
        Item {rowIndex},{columnIndex}
      </div>
    );


    render() {
      return (
              <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
              <Modal.Header>
                  <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
              </Modal.Header>
              <Modal.Body>
              <Grid
                  columnCount={this.columnCount}
                  columnWidth={index => this.columnWidths[index]}
                  height={150}
                  rowCount={this.rowCount}
                  rowHeight={index => this.rowHeights[index]}
                  width={400}
                >
                  {this.Cell}
                </Grid>
              </Modal.Body>
              <Modal.Footer>
                  <Button variant="secondary" onClick={this.onClose}>Accept</Button>
                  <Button variant="secondary" onClick={this.load}>Load</Button>
              </Modal.Footer>
              </Modal>
      );
    }
}


GraphView.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
    onClose: propTypes.func,
}
