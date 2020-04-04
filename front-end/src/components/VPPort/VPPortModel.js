import { DefaultPortModel } from '@projectstorm/react-diagrams';
import { VPLinkFactory } from '../VPLink/VPLinkFactory';

export class VPPortModel extends DefaultPortModel {

      createLinkModel() {
          const factory = new VPLinkFactory();
          return factory.generateModel();
      }

      canLinkToPort(port) {
          // can't both be in or out ports
          return port instanceof VPPortModel
              && this.options.in !== port.options.in;
      }
}
