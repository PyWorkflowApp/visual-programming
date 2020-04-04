import * as React from 'react';
import { AbstractReactFactory } from '@projectstorm/react-canvas-core';
import CustomNodeModel from './CustomNodeModel';
import CustomNodeWidget from './CustomNodeWidget';

export default class CustomNodeFactory extends AbstractReactFactory {
    constructor() {
        super('custom-node');
    }

    generateModel(event) {
        return new CustomNodeModel(event.initialConfig.options, event.initialConfig.config);
    }

    generateReactWidget(event) {
        return <CustomNodeWidget engine={this.engine} node={event.model} />;
    }
}
