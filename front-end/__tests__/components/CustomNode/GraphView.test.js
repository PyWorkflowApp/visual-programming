import React from 'react'
import renderer from 'react-test-renderer';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import GraphView from '../../../src/components/CustomNode/GraphView';

describe('Validate Graph Modal', () => {
  it('Display warning message', () => {
    const node = new CustomNodeModel({id: "myId"});
    const graphView = renderer.create(
      <GraphView node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}}  />
    ).toJSON();
    expect(graphView).toMatchSnapshot();
  });
});
