import React from 'react'
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import createEngine from '@projectstorm/react-diagrams';


describe('Validates CustomNodeModel', () => {
  it('Validates serialization/deserialization', () => {
    const node = new CustomNodeModel({id: "myId", num_in: 2, num_out: 1});
    node.setStatus("Complete");
    const engine = createEngine();
    const serializedModel = node.serialize();

    const otherNode = new CustomNodeModel();
    otherNode.deserialize(serializedModel, engine);

    expect(otherNode).toStrictEqual(node);
  });
});
