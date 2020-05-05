import React from 'react'
import { render } from '@testing-library/react'
import About from '../../src/components/About';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates About', () => {
  it('Does not display About info', () => {
    const app = render(<About show={false} />);
    expect(app).toMatchSnapshot();
  });

  it('Displays About info', () => {
    const app = render(<About show={true} />);
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
    about.handleClose();

    expect(event.preventDefault.mock.calls.length).toBe(1);
  });
});
