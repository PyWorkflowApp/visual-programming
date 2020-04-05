import * as React from 'react';
import { CustomLinkModel } from './CustomLinkModel';
import { CustomLinkWidget } from './CustomLinkWidget';
import { DefaultLinkFactory } from '@projectstorm/react-diagrams';

export class CustomLinkFactory extends DefaultLinkFactory {
    constructor() {
        super('advanced');
    }

    generateModel() {
      return new CustomLinkModel();
    }

    generateLinkSegment(model, selected, path) {
        return (
          <g>
            <CustomLinkWidget model={model} path={path} />
          </g>
        );
    }
}
