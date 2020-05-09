import React from 'react'
import { shallow, mount } from 'enzyme';
import OptionInput from '../../../../src/components/CustomNode/Input/OptionInput';

describe('Validates OptionInput', () => {
  it('Display OptionInput', () => {
    const optionInput = shallow(<OptionInput isFlow={false} />);
    expect(optionInput).toMatchSnapshot();
  });
});
