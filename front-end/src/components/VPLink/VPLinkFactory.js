import { DefaultLinkFactory } from '@projectstorm/react-diagrams';
import VPLinkModel from './VPLinkModel';

export default class VPLinkFactory extends DefaultLinkFactory {

    generateModel() {
        return new VPLinkModel();
    }
}
