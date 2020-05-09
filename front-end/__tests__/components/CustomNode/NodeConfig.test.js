import React from 'react'
import { Col, Modal, Button, Form } from 'react-bootstrap';
import { render } from '@testing-library/react'
import { shallow, mount } from 'enzyme';
import CustomNodeModel from '../../../src/components/CustomNode/CustomNodeModel';
import NodeConfig from '../../../src/components/CustomNode/NodeConfig';
import OptionInput from '../../../src/components/CustomNode/NodeConfig';
import FileUploadInput from '../../../src/components/CustomNode/NodeConfig';
import SimpleInput from '../../../src/components/CustomNode/NodeConfig';
import BooleanInput from '../../../src/components/CustomNode/NodeConfig';
import FlowVariableOverride from '../../../src/components/CustomNode/NodeConfig';
import SelectInput from '../../../src/components/CustomNode/NodeConfig';

global.console = {log: jest.fn()}

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

  it('Validates OptionInput with properties', () => {
    const optionInputRendered = render(<OptionInput
        keyName={"keyName"}
        node={{ options: { is_global: true }, config: {description: "Node description"}}}
        flowValue={true}
        />);

    expect(optionInputRendered).toMatchSnapshot();
  });

  it('Display FileUploadInput', () => {
    const fileUploadInput = render(<FileUploadInput />);
    expect(fileUploadInput).toMatchSnapshot();
  });

  it('Display SimpleInput', () => {
    const simpleInput = render(<SimpleInput />);
    expect(simpleInput).toMatchSnapshot();
  });

  it('Display BooleanInput', () => {
    const booleanInput = render(<BooleanInput />);
    expect(booleanInput).toMatchSnapshot();
  });

  it('Display FlowVariableOverride', () => {
    const variableOverride = render(<FlowVariableOverride />);
    expect(variableOverride).toMatchSnapshot();
  });

  it('Display SelectInput', () => {
    const selectInput = render(<SelectInput
                          keyName="myKeyName"
                        />);
    expect(selectInput).toMatchSnapshot();
  });
})
