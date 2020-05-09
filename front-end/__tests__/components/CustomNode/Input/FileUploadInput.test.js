import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUploadInput from '../../../../src/components/CustomNode/Input/FileUploadInput';

describe('Validates FileUploadInput', () => {
  it('Display FileUploadInput', () => {
    const input = shallow(<FileUploadInput />);
    expect(input).toMatchSnapshot();
  });

  it('FileUploadInput selects a file', () => {
    const onChange = jest.fn(() => []);
    const input = mount(<FileUploadInput
                        keyName="uploadFile"
                        onChange={onChange}
                        />);

    const event = { preventDefault: jest.fn(() => [])};
    input.find({keyName: "uploadFile"}).simulate('change', event);
    expect(event.preventDefault.mock.calls.length).toBe(1);
    input.update();

  });
});
