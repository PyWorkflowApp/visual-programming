import React from 'react';
import { Roller } from 'react-spinners-css';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';
import { VariableSizeGrid as Grid } from 'react-window';
import * as API from "../../API";
import '../../styles/GraphView.css';


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


    render() {
      let body;
      let footer;

      if (this.state.loading) {
          // Print loading message
          body = (<Roller color="black" />);
      } else if (this.state.columns.length < 1) {
          // Print instructions about loading
          body = "Loading the data might take a while depending on how big the data is.";
          footer = (
              <Modal.Footer>
                <Button variant="secondary" onClick={this.onClose}>Cancel</Button>
                <Button variant="secondary"
                        disabled={this.props.node.options.status !== "complete"}
                        onClick={this.load}>Load
                </Button>
              </Modal.Footer>
          );
      } else {
          // Display the grid
          body = (
              <Grid
                  ref={this.state.gridRef}
                  className="Grid"
                  columnCount={this.state.columns.length}
                  columnWidth={index => this.columnWidths(index)}
                  height={500}
                  rowCount={this.state.rows.length}
                  rowHeight={index => 20}
                  width={800}
              >
                {this.Cell}
              </Grid>
          );
      }

      return (
          <Modal
              show={this.props.show}
              onHide={this.props.toggleShow}
              refreshData={this.props.refreshData}
              centered
              onWheel={e => e.stopPropagation()}
          >
              <Modal.Header closeButton>
                   <Modal.Title><b>{this.props.node.options.name}</b> View</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                  {body}
              </Modal.Body>
              {footer}
          </Modal>
      );
    }
}


GraphView.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
    onClose: propTypes.func,
};
