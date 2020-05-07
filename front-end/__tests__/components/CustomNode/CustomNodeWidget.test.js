import React from 'react'
import createEngine from '@projectstorm/react-diagrams';
import { render } from '@testing-library/react'
import ReactDOM from 'react-dom';
import CustomNodeWidget from '../../../src/components/CustomNode/CustomNodeWidget';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';

describe('Validate CustomNodeWidget', () => {

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

    const createElement = document.createElement.bind(document);
document.createElement = (tagName) => {
    if (tagName === 'canvas') {
        return {
            getContext: () => ({}),
            measureText: () => ({})
        };
    }
    return createElement(tagName);
};

  });

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

  it('Validates CustomNodeWidget', () => {
    const node = new CustomNodeModel({id: "myId"});
    const model = {
      node: node,
      globals: {}
    };
    const engine = createEngine();
    engine.setModel(model);

    const div = document.createElement('div');
    const nodeWidget = ReactDOM.render(<CustomNodeWidget
        engine={engine}
        node={node}/>, div);

    expect(nodeWidget.state.showConfig).toBe(false);
    expect(nodeWidget.state.showGraph).toBe(false);

    nodeWidget.toggleConfig();
    nodeWidget.toggleGraph();

    expect(nodeWidget.state.showConfig).toBe(true);
    expect(nodeWidget.state.showGraph).toBe(true);

    nodeWidget.handleDelete();

    expect(global.fetch.mock.calls.length).toBe(1);

    nodeWidget.acceptConfiguration({}, {});
    expect(global.fetch.mock.calls.length).toBe(2);

  });
})
