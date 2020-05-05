import React from 'react'
import { render } from '@testing-library/react'
import CustomNodeFactory from '../../../src/components/CustomNode/CustomNodeFactory';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import CustomNodeWidget from '../../../src/components/CustomNode/CustomNodeWidget';

describe('Validate CustomNodeFactory', () => {
  it('CustomNodeFactory generates CustomNodeWidget', () => {
    const customNodeFactory = new CustomNodeFactory();
    const node = new CustomNodeModel({id: "myId"});
    const model = {
      node: node,
    };
    const event = {
      model: model,
    };
    const widget = customNodeFactory.generateReactWidget(event);
    expect(widget instanceof CustomNodeWidget).toBe(true);
  });
})
