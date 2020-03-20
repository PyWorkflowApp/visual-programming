import * as React from 'react';
import { CustomNodeModel } from './CustomNodeModel';
import { CustomNodeWidget } from './CustomNodeWidget';
import { AbstractReactFactory } from '@projectstorm/react-canvas-core';


export class CustomNodeFactory extends AbstractReactFactory {
    constructor() {
        super('advanced');
    }

    generateModel(): CustomLinkModel {
      return new CustomLinkModel();
    }

    generateLinkSegment(model: CustomLinkModel, selected: boolean, path: string) {
        return (
          <g>
            <CustomLinkModel model={model} path={path} />
          </g>
        );
    }
}
