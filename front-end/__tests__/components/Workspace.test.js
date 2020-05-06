import React from 'react'
import { render } from '@testing-library/react'
import Workspace from '../../src/components/Workspace';
import FileUpload from '../../src/components/Workspace';

global.console = {log: jest.fn()}
global.confirm = () => true;

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates Workspace initialization', () => {
  it('Creates Workspace', () => {
    const workspace = render(<Workspace />);
    expect(workspace).toMatchSnapshot();
  });

  it('Validates Workspace', () => {
    const workspace = new Workspace();
    workspace.componentDidMount();
    workspace.getAvailableNodes();
    workspace.getGlobalVars();
    workspace.clear();
    workspace.execute();

    expet(globa.fetch.mock.calls.length).toBe(3);
  });

  it('Display FileUpload', () => {
    const fileUpload = render(<FileUpload />);
    expect(fileUpload).toMatchSnapshot();
  });
});
