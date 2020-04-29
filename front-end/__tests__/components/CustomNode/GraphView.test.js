import React from 'react'
import { render } from '@testing-library/react'
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import GraphView from '../../../src/components/CustomNode/GraphView';

describe('Validate Graph Modal', () => {
  it('Display warning message', () => {
    const node = new CustomNodeModel({id: "myId"});
    const graphView = render(
      <GraphView node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}}  />
    );
    expect(graphView).toMatchSnapshot();
  });
});
