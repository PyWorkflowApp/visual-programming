import React from 'react'
import { downloadFile } from '../src/utils';

describe('Validates downloadFile', () => {
  global.URL.createObjectURL = jest.fn();
  global.URL.revokeObjectURL = jest.fn();

  const object = {
    click: jest.fn(),
  };

  global.document.createElement = jest.fn((tag) => object);

  it('Validate urls', () => {
    global.URL.createObjectURL = jest.fn(() => 'http://localhost:8080/');
    const createElementMock = jest.fn((type)=>{})
    Object.defineProperty(document, 'createElement', createElementMock);

    downloadFile("{request:data}", "application/json", "diagram.json");
    expect(object.click.mock.calls.length).toBe(1);
    expect(object.href).toBe('http://localhost:8080/');
  });
});
