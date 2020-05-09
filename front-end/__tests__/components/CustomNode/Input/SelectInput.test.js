import React from 'react'
import { shallow, mount } from 'enzyme';
import SelectInput from '../../../../src/components/CustomNode/Input/SelectInput';

describe('Validates SelectInput', () => {
  it('Display SelectInput', () => {
    const options =["area", "bar", "line", "point"];
    const input = shallow(<SelectInput
          options={options}
          />);
    expect(input).toMatchSnapshot();
  });
});
