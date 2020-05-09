import React from 'react'
import { shallow, mount } from 'enzyme';
import SimpleInput from '../../../../src/components/CustomNode/Input/SimpleInput';

describe('Validates SimpleInput', () => {
  it('Display SimpleInput', () => {
    const input = shallow(<SimpleInput />);
    expect(input).toMatchSnapshot();
  });

  it('Display SimpleInput as number', () => {
    const changeFn = jest.fn(() => []);
    const input = mount(<SimpleInput
          type="number"
          keyName="numberInput"
          onChange={changeFn}
          disabled={false}
          />);

    expect(changeFn.mock.calls.length).toBe(1);
    input.find({keyName: "numberInput"}).simulate('change', {target: {value: 654321}})
    expect(changeFn.mock.calls.length).toBe(2);
  });
});
