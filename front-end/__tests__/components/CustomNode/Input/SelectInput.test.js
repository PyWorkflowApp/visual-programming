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

  it('SelectInput onChange', () => {
    const onChange = jest.fn(() => []);
    const options =["area", "bar", "line", "point"];
    const input = mount(<SelectInput
          options={options}
          onChange={onChange}
          value="area"
          keyName="selectInputPlot"
          />);

    expect(onChange.mock.calls.length).toBe(1);
    input.find({keyName: "selectInputPlot"}).simulate('change', {target: {value: "bar"}})

    expect(onChange.mock.calls.length).toBe(2);
  });
});
