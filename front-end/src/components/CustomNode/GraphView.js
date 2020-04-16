import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';
import { VariableSizeGrid as Grid } from 'react-window';
import  AutoSizer from 'react-virtualized-auto-sizer';
import * as API from "../../API";

export default class GraphView extends React.Component {

    constructor(props) {
      super(props);
      this.key_id = props.node.getNodeId();
      this.state = {
        loading: false,
        rowCount: 0,
        columnCount: 0,
        data: [],
        keys: [],
        gridRef: React.createRef()};
    }

  onResize = (...args) => {
      if (this.state.gridRef.current != null) {
        this.state.gridRef.current.resetAfterIndices({
          columnIndex: 0,
          shouldForceUpdate: false
        });
      }
  };

    load = async () => {
          console.log("Loading data");
          this.setState({loading: true})
          API.retrieveData(this.key_id)
          .then(json => {
            const keys = Object.keys(json);
            const columnCount = keys.length;
            console.log("There are " + columnCount + " columns");
            const rows = Object.keys(json[keys[0]]);
            const rowCount = rows.length;
            console.log("There are " + rowCount + " rows")
            this.setState({ data: json,
              keys: keys,
              columnCount: columnCount,
              rowCount: rowCount,
              loading: false});
          }).catch(err => console.log(err));
    }

    onClose = () => {
        this.props.toggleShow();
    };

    columnWidths = () => new Array(1000)
      .fill(true)
      .map(() => 75 + Math.round(Math.random() * 50));

    rowHeights = () => new Array(765)
      .fill(true)
      .map(() => 25 + Math.round(Math.random() * 50));

    Cell = ({ columnIndex, rowIndex, style }) => {
      if (rowIndex === 0) {
        return (
          <div style={style}>
            {this.state.keys[columnIndex]}
          </div>
        );
      }

      return (<div></div>);

      /*return (
        <div style={style}>
          {this.state.data[this.keys[columnIndex]][rowIndex]}
        </div>
      );*/
    }


    render() {
      if (this.state.loading) {
        return (<div>Loading data...</div>);
      }

      if (this.state.columnCount < 1) {
        return (
          <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
          <Modal.Header>
              <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          Loading the data might take a while depending on how big the data is.
          </Modal.Body>
          <Modal.Footer>
              <Button variant="secondary" onClick={this.onClose}>Accept</Button>
              <Button variant="secondary" onClick={this.load}>Load</Button>
          </Modal.Footer>
          </Modal>
        );
      }

      console.log("Displaying data with " + this.state.columnCount + " columns");
      console.log("Displaying data with " + this.state.rowCount + " rows");

      return (
              <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
              <Modal.Header>
                  <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
              </Modal.Header>
              <Modal.Body>
              <Grid
                  ref={this.state.gridRef}
                  columnCount={this.state.columnCount}
                  columnWidth={index => 40}
                  height={150}
                  rowCount={this.state.rowCount}
                  rowHeight={index => 20}
                  width={480}
                >
                  {this.Cell}
                </Grid>
              </Modal.Body>
              <Modal.Footer>
                  <Button variant="secondary" onClick={this.onClose}>Accept</Button>
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
