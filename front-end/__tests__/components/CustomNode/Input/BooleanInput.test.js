import React from 'react'
import { shallow, mount } from 'enzyme';
import BooleanInput from '../../../../src/components/CustomNode/Input/BooleanInput';

describe('Validates BooleanInpupt', () => {
  it('Display BooleanInput', () => {
    const booleanInput = shallow(<BooleanInput />);
    expect(booleanInput).toMatchSnapshot();
  });
});
