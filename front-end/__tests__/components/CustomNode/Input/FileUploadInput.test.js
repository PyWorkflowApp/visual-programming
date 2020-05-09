import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUploadInput from '../../../../src/components/CustomNode/Input/FileUploadInput';

describe('Validates FileUploadInput', () => {

  beforeEach(() => {
    global.fetch = jest.fn(() => Promise.resolve({
      ok: true,
      data: [],
      json: jest.fn(() => []),
      text: jest.fn(() => Promise.resolve({})),
      headers:{
        get: (s)=>{
          if (s === "content-type") {
            return "text";
          }

          if (s === "Content-Disposition") {
            return "filenameToDownload";
          }
        }
      }
    }));
  });


  it('Display FileUploadInput', () => {
    const input = shallow(<FileUploadInput />);
    expect(input).toMatchSnapshot();
  });

  it('FileUploadInput selects a file', () => {
    const onChange = jest.fn(() => []);
    const disableFunc = jest.fn(() => []);
    const input = mount(<FileUploadInput
                        keyName="uploadFile"
                        disableFunc={disableFunc}
                        onChange={onChange}
                        />);

    const event = { preventDefault: jest.fn(() => [])};
    input.find({keyName: "uploadFile"}).simulate('change', event);
    expect(event.preventDefault.mock.calls.length).toBe(1);
    input.update();

  });

});
