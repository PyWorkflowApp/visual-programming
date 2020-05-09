import React from 'react'
import { shallow, mount } from 'enzyme';
import FileUpload from '../../src/components/FileUpload';

describe('Validates FileUpload', () => {
  it('Displays FileUpload', () => {
    const load = jest.fn(() => []);
    const fileUpload = shallow(<FileUpload
            handleData={load}/>);

    expect(fileUpload).toMatchSnapshot();
  });

});
