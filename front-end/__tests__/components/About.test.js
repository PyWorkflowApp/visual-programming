import React from 'react'
import { render } from '@testing-library/react'
import ReactDOM from 'react-dom';
import About from '../../src/components/About';

global.console = {error: jest.fn()}

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates About', () => {
  it('Does not display About info', () => {
    const div = React.createElement('div');
    const app = render(<About show={false} />, div);
    expect(app).toMatchSnapshot();
  });

  it('Displays About info', () => {
    const div = React.createElement('div');
    const app = render(<About show={true} />, div);
    expect(app).toMatchSnapshot();
  });

  it('Validates closing', () => {
    const props = {
      show: true
    };

    const event = {
      preventDefault: jest.fn(() => [])
    };

    const about = new About(props);
    about.componentDidMount();
    about.handleShow(event);
    about.handleClose();

    expect(event.preventDefault.mock.calls.length).toBe(1);
  });
});
