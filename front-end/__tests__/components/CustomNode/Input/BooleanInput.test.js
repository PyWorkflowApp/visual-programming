import React from 'react'
import { shallow, mount } from 'enzyme';
import BooleanInput from '../../../../src/components/CustomNode/Input/BooleanInput';

describe('Validates BooleanInpupt', () => {
  it('Display BooleanInput', () => {
    const booleanInput = shallow(<BooleanInput />);
    expect(booleanInput).toMatchSnapshot();
  });

  it('Checked BooleanInput', () => {
    const booleanInput = shallow(<BooleanInput
                        keyName="booleanSelector"
                        value={false}/>);

    expect(booleanInput.find({name: "booleanSelector"}).prop('checked')).toBe(false);

    booleanInput.find({name: "booleanSelector"}).simulate('change', {target: {checked: true}})

    booleanInput.update();
    expect(booleanInput.find({name: "booleanSelector"}).prop('checked')).toBe(true);
  });
});
