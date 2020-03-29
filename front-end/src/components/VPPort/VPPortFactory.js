import { VPPortModel } from './VPPortModel';
import { DefaultPortFactory } from '@projectstorm/react-diagrams';

export class VPPortFactory extends DefaultPortFactory {

    getType() {
        return "vp-port";
    }
    generateModel(event) {
        return new VPPortModel({name: 'vp-port-name'});
    }
}
