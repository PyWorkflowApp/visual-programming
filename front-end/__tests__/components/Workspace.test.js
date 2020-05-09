import React from 'react'
import { Container } from 'react-bootstrap';
import { render } from '@testing-library/react'
import { shallow, mount } from 'enzyme';
import Workspace from '../../src/components/Workspace';
import { CanvasWidget } from '@projectstorm/react-canvas-core';

jest.mock('@projectstorm/react-canvas-core', () => (
  {
    ...(jest.requireActual('@projectstorm/react-canvas-core')),
    CanvasWidget: () => <div />
  }
))

global.console = {log: jest.fn(() => []), error: jest.fn(() => [])}
global.confirm = () => true;

const createElement = document.createElement.bind(document);

document.createElement = (tagName) => {
if (tagName === 'canvas') {
    return {
        getContext: () => ({}),
        measureText: () => ({})
    };
}
return createElement(tagName);
};

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


  it('Displays Workspaces', () => {
    const workspace = shallow(
          <Workspace />
    );

    workspace.find('Button').at(0).simulate('click');
    workspace.find('Button').at(1).simulate('click');
    workspace.find('Button').at(2).simulate('click');

  });

});
