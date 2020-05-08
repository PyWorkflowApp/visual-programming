import React from 'react'
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import CustomNodeFactory from '../../../src/components/CustomNode/CustomNodeFactory';
import VPPortFactory from '../../../src/components/VPPort/VPPortFactory';
import createEngine from '@projectstorm/react-diagrams';


describe('Validates CustomNodeModel', () => {
  it('Validates serialization/deserialization', () => {
    const node = new CustomNodeModel({id: "myId", num_in: 2, num_out: 1});
    node.setStatus("Complete");
    const engine = createEngine();
    engine.getNodeFactories().registerFactory(new CustomNodeFactory());
    engine.getPortFactories().registerFactory(new VPPortFactory());

    const serializedModel = node.serialize();
    const event = {
        data: serializedModel,
        engine: engine,
        registerModel: jest.fn(() => [])
    };
    const otherNode = new CustomNodeModel();
    otherNode.deserialize(event, engine);

    expect(event.registerModel.mock.calls.length).toBe(4);
  });
});
