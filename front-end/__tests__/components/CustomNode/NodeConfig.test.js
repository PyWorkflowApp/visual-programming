import React from 'react'
import { render } from '@testing-library/react'
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import NodeConfig from '../../../src/components/CustomNode/NodeConfig';
import OptionInput from '../../../src/components/CustomNode/NodeConfig';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

global.confirm = (s) => true;

describe('Validate NodeConfig Modal', () => {
  it('Display configuration', () => {
    const node = new CustomNodeModel({id: "myId"});
    const nodeConfig = render(
      <NodeConfig node={node}
          show={true}
          toggleShow={() => {}}
          onDelete={() => {}}
          onSubmit={() => {}}  />
    );
    expect(nodeConfig).toMatchSnapshot();
  });

  it('Validates handleDelete',() => {
    const props = {
      onDelete: jest.fn(() => []),
      toggleShow: jest.fn(() => [])
    };

    const nodeConfig = new NodeConfig(props);
    nodeConfig.handleDelete();

    expect(props.onDelete.mock.calls.length).toBe(1);
    expect(props.toggleShow.mock.calls.length).toBe(1);
  });

  it('Validates handleSubmit', () => {
    const props = {
      onSubmit: jest.fn(() => []),
      toggleShow: jest.fn(() => [])
    };

    const event = {
        preventDefault: jest.fn(() => [])
    };

    const nodeConfig = new NodeConfig(props);
    nodeConfig.handleSubmit(event);

    expect(event.preventDefault.mock.calls.length).toBe(1);
    expect(props.onSubmit.mock.calls.length).toBe(1);
    expect(props.toggleShow.mock.calls.length).toBe(1);
  });

  it('Display OptionInput', () => {
    const optionInput = render(<OptionInput />);
    expect(optionInput).toMatchSnapshot();
  });
})
