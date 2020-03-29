import { DefaultPortModel } from '@projectstorm/react-diagrams';
import { VPLinkModel } from '../VPLink/VPLinkModel';

export class VPPortModel extends DefaultPortModel {
      createLinkModel() {
          return new VPLinkModel();
      }

      canLinkToPort(port) {
        return port instanceof VPPortModel;
      }
}
