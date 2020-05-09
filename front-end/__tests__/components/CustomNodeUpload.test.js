import React from 'react'
import { render } from '@testing-library/react'
import { shallow, mount } from 'enzyme';
import { DiagramModel } from '@projectstorm/react-diagrams';
import CustomNodeUpload from '../../src/components/CustomNodeUpload';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates CustomNodeUpload', () => {
  it('Displays CustomNodeUpload', () => {
    const onUpload = jest.fn(() => []);
    const nodeUpload = render(<CustomNodeUpload
          onUpload={onUpload}
            />);
    expect(nodeUpload).toMatchSnapshot();
  });

  it('Validates uploading a file', () => {
    const onUpload = jest.fn(() => []);
    const nodeUpload = new CustomNodeUpload(onUpload);
    nodeUpload.input = {
      current: {
        files: ["randomFile"]
      }
    };

    const event = {
      preventDefault: jest.fn(() => [])
    }
    nodeUpload.onFileSelect(event);

    expect(event.preventDefault.mock.calls.length).toBe(1);
  });

  it('Validate loading message', () => {
    const onUpload = jest.fn(() => []);
    const nodeUpload = shallow(<CustomNodeUpload
          onUpload={onUpload}
            />);

    nodeUpload.setState({status: "loading"});
    nodeUpload.update();
    expect(nodeUpload.html()).toContain("<div>Uploading file...</div>");

  });

  it('Validate failed message', () => {
    const onUpload = jest.fn(() => []);
    const nodeUpload = shallow(<CustomNodeUpload
          onUpload={onUpload}
            />);

    nodeUpload.setState({status: "failed"});
    nodeUpload.update();
    expect(nodeUpload.html()).toContain("<div>Upload failed. Try a new file.</div>");

  });
});
