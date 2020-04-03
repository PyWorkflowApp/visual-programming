import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import propTypes from 'prop-types';
import { VariableSizeGrid as Grid } from 'react-window';

function GraphView(props) {

    const onClose = () => {
        props.toggleShow();
    };

    /*
    * Dummy example taken from https://react-window.now.sh/#/examples/grid/variable-size
    */
    const columnWidths = new Array(1000)
      .fill(true)
      .map(() => 75 + Math.round(Math.random() * 50));

    const rowHeights = new Array(1000)
      .fill(true)
      .map(() => 25 + Math.round(Math.random() * 50));

    const Cell = ({ columnIndex, rowIndex, style }) => (
      <div style={style}>
        Item {rowIndex},{columnIndex}
      </div>
    );


    return (
            <Modal show={props.show} onHide={props.toggleShow} centered>
            <Modal.Header>
                <Modal.Title><b>{props.node.options.name}</b> View</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Grid
                columnCount={1000}
                columnWidth={index => columnWidths[index]}
                height={150}
                rowCount={1000}
                rowHeight={index => rowHeights[index]}
                width={400}
              >
                {Cell}
              </Grid>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onClose}>Accept</Button>
            </Modal.Footer>
            </Modal>
    );
}


GraphView.propTypes = {
    show: propTypes.bool,
    toggleShow: propTypes.func,
    onClose: propTypes.func,
}

export default GraphView;
