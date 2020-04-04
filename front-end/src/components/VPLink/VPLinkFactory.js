import { VPLinkModel } from './VPLinkModel';
import { DefaultLinkFactory } from '@projectstorm/react-diagrams';

export class VPLinkFactory extends DefaultLinkFactory {

    generateModel() {
        return new VPLinkModel();
    }
}
