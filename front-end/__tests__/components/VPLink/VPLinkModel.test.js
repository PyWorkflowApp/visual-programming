import React from 'react'
import VPLinkModel from '../../../src/components/VPLink/VPLinkModel';
// import * as API from '../../../src/API';
jest.mock('../../../src/API');

describe('VPLinkModel behaves as expected', () => {
  it('Determine if default is last position', () => {
      const linkModel = new VPLinkModel();
      expect(linkModel.isLastPositionDefault()).toBe(true);
  });
  it('remove calls deleteEdge API', () => {
    const linkModel = new VPLinkModel();
    linkModel.remove();
    expect(API.calls.length).toBe(1);
  });
});
