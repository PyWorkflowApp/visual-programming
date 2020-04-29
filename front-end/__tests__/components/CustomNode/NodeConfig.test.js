import React from 'react'
import { render } from '@testing-library/react'
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import NodeConfig from '../../../src/components/CustomNode/NodeConfig';


describe('Validate NodeConfig Modal', () => {
  it('Display configuration', () => {
    const node = new CustomNodeModel({id: "myId"});
    const nodeConfig = render(
      <NodeConfig node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}}  />
    );
    expect(nodeConfig).toMatchSnapshot();
  });
})
