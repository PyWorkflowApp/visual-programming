import React from 'react'
import { render } from '@testing-library/react'
import App from '../../src/components/App';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates App initialization', () => {
  it('Creates App', () => {
    const app = render(<App />);
    expect(app).toMatchSnapshot();
  });
});
