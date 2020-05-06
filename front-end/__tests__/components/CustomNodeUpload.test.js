import React from 'react'
import { render } from '@testing-library/react'
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
    nodeUpload.onFileSelect();
  });
});
