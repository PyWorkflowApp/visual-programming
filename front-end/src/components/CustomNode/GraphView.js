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
              rowCount: rowCount });
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
      console.log("Showing (" + columnIndex + ", " + rowIndex + ") out of (" + this.state.columnCount + ", " + this.state.rowCount + ")");
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
      if (this.state.columnCount < 1) {
        return (
          <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
          <Modal.Header>
              <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
          </Modal.Header>
          <Modal.Body>
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
              <div style={{height: '150px', width: '16000px', overflow: 'scroll' }}>
              <AutoSizer onResize={this.onResize}>
               {({height, width}) => (
              <Grid
                  ref={this.state.gridRef}
                  columnCount={this.state.columnCount}
                  columnWidth={index => 20}
                  height={height}
                  rowCount={this.state.rowCount}
                  rowHeight={index => this.rowHeights[index]}
                  width={width}
                >
                  {this.Cell}
                </Grid>
              )}
                </AutoSizer>
                </div>
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
