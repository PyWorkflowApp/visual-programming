import React from 'react'
import { shallow, mount } from 'enzyme';
import SimpleInput from '../../../../src/components/CustomNode/Input/SimpleInput';

describe('Validates SimpleInput', () => {
  it('Display SimpleInput', () => {
    const input = shallow(<SimpleInput />);
    expect(input).toMatchSnapshot();
  });
});
