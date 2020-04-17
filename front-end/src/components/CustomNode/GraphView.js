import React, { forwardRef } from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';
import { VariableSizeGrid as Grid } from 'react-window';
import * as API from "../../API";
import '../../styles/index.css';


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

  columnWidths = (index) => {
    return 10 * this.state.widths[index];
  }

  rowHeights = () => new Array(765)
    .fill(true)
    .map(() => 25 + Math.round(Math.random() * 50));

  onClose = () => {
        this.props.toggleShow();
  };

  computeWidths = (columnCount, rowCount, json) => {
    const widths = new Array(columnCount);
    const keys = Object.keys(json);
    for (let index = 0; index < columnCount; index++) {
        const key = keys[index];
        widths[index] = key.length;
        for (let rowIndex = 0; rowIndex < rowCount; rowIndex++) {
          const value = json[key][rowIndex.toString()];
          if (value != null && value.length > widths[index]) {
            widths[index] = value.length;
          }
        }
    }

    return widths;
  }

  load = async () => {
          this.setState({loading: true})
          API.retrieveData(this.key_id)
          .then(json => {
            const keys = Object.keys(json);
            const columnCount = keys.length;
            const rows = Object.keys(json[keys[0]]);
            const rowCount = rows.length;
            const widths = this.computeWidths(columnCount, rowCount, json);
            this.setState({ data: json,
              keys: keys,
              columnCount: columnCount,
              rowCount: rowCount,
              loading: false,
              widths: widths});
          }).catch(err => console.log(err));
    }

    Cell = ({ columnIndex, rowIndex, style }) => {
      const className =  columnIndex % 2
          ? rowIndex % 2 === 0
            ? 'GridItemOdd'
            : 'GridItemEven'
          : rowIndex % 2
            ? 'GridItemOdd'
            : 'GridItemEven';

      if (rowIndex === 0) {
        return (
          <div className={className} style={style}>
            {this.state.keys[columnIndex]}
          </div>
        );
      }

      return (
        <div className={className} style={style}>
          {this.state.data[this.state.keys[columnIndex]][rowIndex.toString()] }
        </div>
      );
    }

    preventDefault = (e) => {
      e = e || window.event;
      e.stopPropagation();
    }

    outerElementType = forwardRef((props, ref) => (
        <div ref={ref} onWheel={this.preventDefault} {...props} />
    ));

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

      return (
              <Modal show={this.props.show} onHide={this.props.toggleShow} centered>
              <Modal.Header>
                  <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
              </Modal.Header>
              <Modal.Body>
              <Grid
                  ref={this.state.gridRef}
                  className="Grid"
                  columnCount={this.state.columnCount}
                  columnWidth={index => this.columnWidths(index)}
                  height={150}
                  rowCount={this.state.rowCount}
                  rowHeight={index => 20}
                  width={480}
                  outerElementType={this.outerElementType}
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
