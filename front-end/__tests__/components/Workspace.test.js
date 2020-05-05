import React from 'react'
import { render } from '@testing-library/react'
import Workspace from '../../src/components/Workspace';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates Workspace initialization', () => {
  it('Creates Workspace', () => {
    const workspace = render(<Workspace />);
    expect(workspace).toMatchSnapshot();
  });
});
