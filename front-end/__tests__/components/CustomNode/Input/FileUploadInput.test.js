import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUploadInput from '../../../../src/components/CustomNode/Input/FileUploadInput';

describe('Validates FileUploadInput', () => {
  it('Display FileUploadInput', () => {
    const input = shallow(<FileUploadInput />);
    expect(input).toMatchSnapshot();
  });
});
