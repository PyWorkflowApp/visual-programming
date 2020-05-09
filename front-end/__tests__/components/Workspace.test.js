import React from 'react'
import { Container } from 'react-bootstrap';
import { render } from '@testing-library/react'
import { shallow, mount } from 'enzyme';
import Workspace from '../../src/components/Workspace';

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

/*
  it('Displays Workspaces', () => {
    const workspace = shallow(
      <Container fluid={true} className="App">
          <Workspace />
      </Container>
    );
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
  */
});
