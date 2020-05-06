import React from 'react'
import { render } from '@testing-library/react'
import * as API from '../../src/API';
import VPLinkModel from '../../src/components/VPLink/VPLinkModel';
import CustomNodeModel from '../../src/components/CustomNode/CustomNodeModel';
import VPPortModel from '../../src/components/VPPort/VPPortModel'

describe('Validates API calls', () => {

  beforeEach(() => {
    global.fetch = jest.fn(() => Promise.resolve({
      ok: true,
      data: [],
      json: jest.fn(() => [])
    }));
  });

  it('Validates executionOrder', () => {
    API.executionOrder();
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual({});
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/execute");
  });

  it('Validates execute', () => {
    const node = {
      options: {
        id: 'nodeId'
      }
    };

    API.execute(node);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual({});
    expect(global.fetch.mock.calls[0][0]).toBe("/node/nodeId/execute");
  });

  it('Validates retrieveData', () => {
    API.retrieveData("nodeId");
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual({});
    expect(global.fetch.mock.calls[0][0]).toBe("/node/nodeId/retrieve_data");
  });

  it('Validates downloadDataFile', () => {
    const node = {
      options: {
        id: 'nodeId'
      },
      config: {}
    };

    API.downloadDataFile(node);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/download");
  });

  it('Validates uploadDataFile', () => {
    const formData = { data: {}};
    const options = {method: "POST", body: formData};
    API.uploadDataFile(formData);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual(options);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/upload");
  });

  it('Validates deleteEdge', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    const targetModel = new CustomNodeModel({id: "myId2", num_in: 2, num_out: 1});

    const sourcePort = new VPPortModel({name: 'source-port-name'});
    sourcePort.setParent(sourceModel);
    const targetPort = new VPPortModel({name: 'target-port-name'});
    targetPort.setParent(targetModel);
    const linkModel = new VPLinkModel();
    linkModel.setSourcePort(sourcePort);
    linkModel.setTargetPort(targetPort);

    const options = {method: "POST"};
    API.deleteEdge(linkModel);

    expect(global.fetch.mock.calls.length).toBe(2);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual(options);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/edge/myId1/myId2");

  });

});
