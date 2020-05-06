import React from 'react'
import { render } from '@testing-library/react'
import { DiagramModel } from '@projectstorm/react-diagrams';
import GlobalFlowMenu from '../../src/components/GlobalFlowMenu';

global.fetch = jest.fn(() => Promise.resolve({
  data: [],
  json: jest.fn(() => [])
}));

describe('Validates GlobalFlowMenu', () => {
  it('Display of GlobalFlowMenu with empty list', () => {
    const model = new DiagramModel();
    const globals = [];
    const menuItems = [];
    const getGlobalVars = jest.fn(() => []);
    const globalFlowMenu = render(<GlobalFlowMenu
                  menuItems={menuItems}
                  nodes={globals}
                  diagramModel={model}
                  onUpdate={getGlobalVars}
                  />);
    expect(globalFlowMenu).toMatchSnapshot();
  });

  it('Validates execution of methods', () => {
    const flowMenu = new GlobalFlowMenu();
    const data = {}
    flowMenu.handleEdit(data);
  });
});
