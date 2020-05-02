import React from 'react';
import { VegaLite } from 'react-vega';
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
      data: [],
      rows: [],
      columns: [],
      maxWidth: 0,
      gridRef: React.createRef()};
  };

  columnWidths = (index) => {
    return 10 * this.state.widths[index];
  };

  rowHeights = () => new Array(765)
    .fill(true)
    .map(() => 25 + Math.round(Math.random() * 50));

  onClose = () => {
        this.props.toggleShow();
  };

  /**
   * Compute width of grid columns.
   *
   * Width is based on the maximum-length cell contained within the JSON data.
   *
   * @param {Object} columns The column information from the data
   * @param {int} rowCount Number of rows in the data
   * @param {Object} data The raw data from Node execution
   * @returns {any[]}
   */
    computeWidths = (columns, rowCount, data) => {
        const columnCount = columns.length;
        const widths = new Array(columnCount);
        let maxWidth = this.state.maxWidth;

        for (let index = 0; index < columnCount; index++) {
            const column = columns[index];
            widths[index] = column.length;

            for (let rowIndex = 0; rowIndex < rowCount; rowIndex++) {
              const row = data[column][rowIndex.toString()];

              if (row != null && row.length > widths[index]) {
                widths[index] = row.length;
              }

            maxWidth += widths[index] * 10;
            }
        }

        this.setState({maxWidth: maxWidth});
        return widths;
    };

  load = async () => {
      this.setState({loading: true});

      API.retrieveData(this.key_id)
          .then(json => {
            const columns = Object.keys(json);
            const rows = Object.keys(json[columns[0]]);
            const widths = this.computeWidths(columns, rows.length, json);

            this.setState({
                data: json,
                columns: columns,
                rows: rows,
                loading: false,
                widths: widths
            });
          })
          .catch(err => console.error(err));
  };

  loadGraph = async () => {
      this.setState({loading: true});
      API.retrieveData(this.key_id)
          .then(json => {
              this.setState({
                  data: json,
                  loading: false,
              });
          })
          .catch(err => console.log(err));

  };

    Cell = ({ columnIndex, rowIndex, style }) => {
      const className = (rowIndex % 2 === 0) ? 'GridItemEven' : 'GridItemOdd';
      const column = this.state.columns[columnIndex];

      return (
        <div className={className} style={style}>
          {(rowIndex === 0) ? column : this.state.data[column][rowIndex.toString()]}
        </div>
      );
    };


    render() {
      let body;
      let footer;

      if (this.state.loading) {
          // Print loading spinner
          body = (<Roller color="black" />);
      } else if (this.state.data.length < 1) {
          // Print message to load respective table/graph
          if (this.props.node.options.node_type === "visualization") {
              // Print instructions about loading
              body = "Loading the graph might take a while depending on how big the data is.";
              footer = (
                  <Modal.Footer>
                    <Button variant="secondary" onClick={this.onClose}>Cancel</Button>
                    <Button variant="secondary"
                            disabled={this.props.node.options.status !== "complete"}
                            onClick={this.loadGraph}>Load
                    </Button>
                  </Modal.Footer>
              );
          } else {
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
          }
      } else {
          // Display the visualization
          if (this.props.node.options.node_type === "visualization") {
              // Display the graph
              body = (<VegaLite spec={this.state.data} />);
          } else {
              // Display the grid
              let displayHeight = this.state.rows.length * 20;
              let displayWidth = this.state.maxWidth;

              body = (
                  <Grid
                      ref={this.state.gridRef}
                      className="Grid"
                      columnCount={this.state.columns.length}
                      columnWidth={index => this.columnWidths(index)}
                      height={displayHeight < 600 ? displayHeight + 5 : 600}
                      rowCount={this.state.rows.length}
                      rowHeight={index => 20}
                      width={displayWidth < 900 ? displayWidth : 900}
                  >
                    {this.Cell}
                  </Grid>
              );
          }

      }

      return (
          <Modal
              show={this.props.show}
              onHide={this.props.toggleShow}
              centered
              dialogClassName={"GraphView"}
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
