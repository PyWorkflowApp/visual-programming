import React from 'react'
import { render } from '@testing-library/react'
import { shallow, mount } from 'enzyme';
import { VariableSizeGrid as Grid } from 'react-window';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import GraphView from '../../../src/components/CustomNode/GraphView';

global.console = {log: jest.fn()}

const data = {"AAPL_x": {"0": "2014-01-02", "1": "2014-01-03", "2": "2014-01-06", "3": "2014-01-07", "4": "2014-01-08", "5": "2014-01-09", "6": "2014-01-10", "7": "2014-01-13", "8": "2014-01-14", "9": "2014-01-15", "10": "2014-01-16", "11": "2014-01-17", "12": "2014-01-21", "13": "2014-01-22", "14": "2014-01-23"}, "AAPL_y": {"0": 77.44539475, "1": 77.04557544, "2": 74.89697204, "3": 75.856461, "4": 75.09194679, "5": 76.20263178, "6": 75.2301837, "7": 73.84891755, "8": 75.0113527, "9": 77.14481412, "10": 77.33058367, "11": 76.85652616, "12": 75.39394758, "13": 76.7763823, "14": 76.64038513}};

const response = {
  json: jest.fn(() => {
    return data;
  }),
  ok: true
};

global.fetch = jest.fn(() => Promise.resolve(response));

describe('Validate Graph Modal', () => {
  it('Display warning message', () => {
    const node = new CustomNodeModel({id: "myId"});
    const graphView = render(
      <GraphView node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}}  />
    );
    expect(graphView).toMatchSnapshot();
  });

  it('Display data', (done) => {
    const node = new CustomNodeModel({id: "myId", options:
    { node_type: "Read CSV",
      status: "complete"}});
    const graphView = shallow(<GraphView
      node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}} />);

    expect(graphView.state('loading')).toBe(false);
    graphView.find('Button').at(1).simulate('click');
    expect(graphView.state('loading')).toBe(true);
    setTimeout(()=>{
      graphView.update();
      expect(graphView.state('loading')).toBe(false);
      done();
    }, 1000);
  });
});
