import React from 'react'
import { shallow, mount } from 'enzyme';
import FlowVariableOverride from '../../../../src/components/CustomNode/Input/FlowVariableOverride';

describe('Validates FlowVariableOverride', () => {
  it('Display FlowVariableOverride', () => {
    const override = shallow(<FlowVariableOverride />);
    expect(override).toMatchSnapshot();
  });
});
