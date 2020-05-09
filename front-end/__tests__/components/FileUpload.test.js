import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUpload from '../../src/components/FileUpload';

global.fetch = jest.fn(() => Promise.resolve({
  json: jest.fn(() => []),
  ok: true
}));

global.console = {log: jest.fn()}

describe('Validates FileUpload', () => {
  it('Displays FileUpload', () => {
    const load = jest.fn(() => []);
    const fileUpload = shallow(<FileUpload
            handleData={load}/>);

    expect(fileUpload).toMatchSnapshot();

    const event = {
      preventDefault: jest.fn(() => [])
    };

    fileUpload.setState({input: { current: { files: ["oneFile"]}}});
    fileUpload.find('input').simulate('change', event);

    expect(event.preventDefault.mock.calls.length).toBe(1);
  });

  it('No file selected', () => {
    const load = jest.fn(() => []);
    const fileUpload = shallow(<FileUpload
            handleData={load}/>);

    const event = {
      preventDefault: jest.fn(() => [])
    };

    fileUpload.setState({input: {}});
    fileUpload.find('input').simulate('change', event);

    expect(event.preventDefault.mock.calls.length).toBe(1);
  });

  it('Load file', () => {
    const load = jest.fn(() => []);
    const fileUpload = shallow(<FileUpload
            handleData={load}/>);

    const click = jest.fn(() => []);

    fileUpload.setState({input: { current: { click: click}}});
    fileUpload.find('Button').simulate('click');

    expect(click.mock.calls.length).toBe(1);
  });

});
