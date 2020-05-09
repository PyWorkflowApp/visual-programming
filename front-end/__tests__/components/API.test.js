import React from 'react'
import { render } from '@testing-library/react'
import * as API from '../../src/API';
import VPLinkModel from '../../src/components/VPLink/VPLinkModel';
import CustomNodeModel from '../../src/components/CustomNode/CustomNodeModel';
import VPPortModel from '../../src/components/VPPort/VPPortModel'

global.console = {log: jest.fn()}
global.URL.createObjectURL = jest.fn(() => 'http://localhost:8080/');
global.URL.revokeObjectURL = jest.fn();

describe('Validates API calls', () => {

  beforeEach(() => {
    global.fetch = jest.fn(() => Promise.resolve({
      ok: true,
      data: [],
      json: jest.fn(() => []),
      text: jest.fn(() => Promise.resolve({})),
      headers:{
        get: (s)=>{
          if (s === "content-type") {
            return "text";
          }

          if (s === "Content-Disposition") {
            return "filenameToDownload";
          }
        }
      }
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

  it('Validates addEdge', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    const targetModel = new CustomNodeModel({id: "myId2", num_in: 2, num_out: 1});

    const sourcePort = new VPPortModel({name: 'source-port-name', in: true});
    sourcePort.setParent(sourceModel);
    const targetPort = new VPPortModel({name: 'target-port-name'});
    targetPort.setParent(targetModel);
    const linkModel = new VPLinkModel();
    linkModel.setSourcePort(sourcePort);
    linkModel.setTargetPort(targetPort);

    const options = {method: "POST"};
    API.addEdge(linkModel);

    expect(global.fetch.mock.calls.length).toBe(2);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual(options);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/edge/myId2/myId1");

  });

  it('Validates uploadWorkflow', () => {
    const formData = { data: {}};
    const options = {method: "POST", body: formData};
    API.uploadWorkflow(formData);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][1]).toStrictEqual(options);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/open");
  });

  it('Validates initWorkflow', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    API.initWorkflow(sourceModel);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/new");
  });

  it('Validates getGlobalVars', () => {
    API.getGlobalVars();
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/globals");
  });

  it('Validates getNodes', () => {
    API.getNodes();
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/workflow/nodes");
  });

  it('Validates updateNode', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    API.updateNode(sourceModel);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/myId1");
  });

  it('Validates deleteNode', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    API.deleteNode(sourceModel);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/myId1");
  });

  it('Validates addNode', () => {
    const sourceModel = new CustomNodeModel({id: "myId1", num_in: 2, num_out: 1});
    API.addNode(sourceModel);
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/");
  });

  it('Validates getNode', () => {
    API.getNode("myId1");
    expect(global.fetch.mock.calls.length).toBe(1);
    expect(global.fetch.mock.calls[0][0]).toBe("/node/myId1");
  });

});
