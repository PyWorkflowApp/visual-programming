import { AbstractModelFactory } from '@projectstorm/react-canvas-core';
import VPPortModel from './VPPortModel';

export default class VPPortFactory extends AbstractModelFactory {

    constructor() {
        super("vp-port");
    }

    generateModel() {
        return new VPPortModel({name: 'vp-port-name'});
    }
}
