import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUploadInput from '../../../../src/components/CustomNode/Input/FileUploadInput';
import CustomNodeModel from '../../../../src/components/CustomNode/CustomNodeModel';

describe('Validates FileUploadInput', () => {

  beforeEach(() => {
    global.console = {log: jest.fn(() => []), error: jest.fn(() => [])};

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
    const node = new CustomNodeModel({id: "myId", num_in: 2, num_out: 1, is_global: false});
    const onChange = jest.fn(() => []);
    const disableFunc = jest.fn(() => []);
    const input = mount(<FileUploadInput
                      value="ready"
                      disableFunc={disableFunc}
                      onChange={onChange}
                      node={node}
                       />);
    expect(input).toMatchSnapshot();
  });

  it('FileUploadInput selects a file', () => {
    const node = new CustomNodeModel({id: "myId", num_in: 2, num_out: 1, is_global: false});
    const onChange = jest.fn(() => []);
    const disableFunc = jest.fn(() => []);
    const input = mount(<FileUploadInput
                        keyName="uploadFile"
                        disableFunc={disableFunc}
                        onChange={onChange}
                        node={node}
                        />);

    const event = { preventDefault: jest.fn(() => [])};
    input.find({keyName: "uploadFile"}).simulate('change', event);
    expect(event.preventDefault.mock.calls.length).toBe(1);

  });

});
