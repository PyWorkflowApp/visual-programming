import React from 'react'
import { render } from '@testing-library/react'
import Workspace from '../../src/components/Workspace';
import FileUpload from '../../src/components/Workspace';

global.console = {log: jest.fn(() => []), error: jest.fn(() => [])}
global.confirm = () => true;

describe('Validates Workspace initialization', () => {

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

  it('Creates Workspace', () => {
    const workspace = render(<Workspace />);
    expect(workspace).toMatchSnapshot();
  });

  it('Validates Workspace', () => {
    const workspace = new Workspace();
    workspace.engine = {
      repaintCanvas: jest.fn()
    };

    workspace.componentDidMount();
    workspace.execute();
    workspace.clear();

    expect(global.fetch.mock.calls.length).toBe(3);
  });

  it('Display FileUpload', () => {
    const fileUpload = render(<FileUpload />);
    expect(fileUpload).toMatchSnapshot();
  });
});
