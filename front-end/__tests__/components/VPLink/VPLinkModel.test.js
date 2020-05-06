import React from 'react'
import VPLinkModel from '../../../src/components/VPLink/VPLinkModel';
import VPPortModel from '../../../src/components/VPPort/VPPortModel'
import * as API from '../../../src/API';
jest.mock('../../../src/API');

describe('VPLinkModel behaves as expected', () => {
  it('Determine if default is last position', () => {
      const linkModel = new VPLinkModel();
      expect(linkModel.isLastPositionDefault()).toBe(true);
  });

  it('remove calls deleteEdge API', () => {
    API.deleteEdge.mockResolvedValue(new Promise((resolve, reject) => {}));
    const linkModel = new VPLinkModel();
    linkModel.remove();
    expect(API.deleteEdge.mock.calls.length).toBe(1);
  });

  it('Calls targetPortChanged', () => {
    API.deleteEdge.mockResolvedValue(Promise.resolve({}));
    API.addEdge.mockResolvedValue(Promise.resolve({}));

    const portModel = new VPPortModel({name: 'vp-port-name'});
    const linkModel = new VPLinkModel();
    linkModel.setTargetPort(portModel);
    expect(API.addEdge.mock.calls.length).toBe(1);
  });

  it('getSVGPath skips execution', () => {
      const linkModel = new VPLinkModel();
      linkModel.isLastPositionDefault = jest.fn(() => true);
      linkModel.getSVGPath();
      expect(linkModel.isLastPositionDefault.mock.calls.length).toBe(1);
  });

  it('getSVGPath executes', () => {
      const linkModel = new VPLinkModel();
      linkModel.isLastPositionDefault = jest.fn(() => false);
      linkModel.getSVGPath();
      expect(linkModel.isLastPositionDefault.mock.calls.length).toBe(1);
  });
});
