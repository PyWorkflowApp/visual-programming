import React from 'react'
import createEngine from '@projectstorm/react-diagrams';
import { render } from '@testing-library/react'
import CustomNodeWidget from '../../../src/components/CustomNode/CustomNodeWidget';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';

describe('Validate CustomNodeWidget', () => {
  it('Display CustomNodeWidget', () => {
    const node = new CustomNodeModel({id: "myId"});
    const model = {
      node: node,
      globals: {}
    };
    const engine = createEngine();
    engine.setModel(model);

    const customNodeWidget = render(
      <CustomNodeWidget  engine={engine} node={node} />
    );
    expect(customNodeWidget).toMatchSnapshot();
  });
})
