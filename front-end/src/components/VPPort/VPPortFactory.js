import { VPPortModel } from './VPPortModel';
import { AbstractModelFactory } from '@projectstorm/react-canvas-core';

export class VPPortFactory extends AbstractModelFactory {

    constructor() {
        super("vp-port");
    }

    generateModel() {
        return new VPPortModel({name: 'vp-port-name'});
    }
}
