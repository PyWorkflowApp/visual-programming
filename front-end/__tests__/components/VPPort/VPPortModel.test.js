import React from 'react'
import { DefaultPortModel } from '@projectstorm/react-diagrams';
import VPPortModel from '../../../src/components/VPPort/VPPortModel'
import VPLinkModel from '../../../src/components/VPLink/VPLinkModel';


describe('VPPortModel only links to different VPPortModels', () => {
  it('null is not VPPortModel', () => {
    const portModel = new VPPortModel({name: 'vp-port-name'});
    expect(portModel.canLinkToPort(null)).toBe(false);
  });

  it('DefaultPortModel is not VPPortModel', () => {
    const portModel = new VPPortModel({name: 'vp-port-name'});
    const otherPortModel = new DefaultPortModel({name: 'default-port-name'});
    expect(portModel.canLinkToPort(otherPortModel)).toBe(false);
  });

  it('Cannot link to itself', () => {
    const portModel = new VPPortModel({name: 'vp-port-name'});
    expect(portModel.canLinkToPort(portModel)).toBe(false);
  });

  it('Cannot link empty inputs to empty inputs', () => {
    const portModel = new VPPortModel({name: 'vp-port-flow'});
    const otherPortModel = new DefaultPortModel({name: 'default-port-flow'});
    expect(portModel.canLinkToPort(otherPortModel)).toBe(false);
  });
});

describe('Validate VPLinkModel generated', () => {
  it('VPPortModel generates VPLinkModel',  () => {
    const portModel = new VPPortModel({name: 'vp-port-name'});
    const linkModel = portModel.createLinkModel();
    expect(linkModel instanceof VPLinkModel).toBe(true);
  });
});
