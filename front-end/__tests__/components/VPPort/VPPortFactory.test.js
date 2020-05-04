import React from 'react';
import VPPortFactory from '../../../src/components/VPPort/VPPortFactory';
import VPPortModel from '../../../src/components/VPPort/VPPortModel';


describe('Generates correct port', () => {
  it('VPPortModel is generated', () => {
    const portFactory = new VPPortFactory();
    const portModel = portFactory.generateModel();
    expect(portModel instanceof VPPortModel).toBe(true);
  })
});
