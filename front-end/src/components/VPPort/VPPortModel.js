import { DefaultPortModel } from '@projectstorm/react-diagrams';
import { VPLinkModel } from '../VPLink/VPLinkModel';

export class VPPortModel extends DefaultPortModel {
      createLinkModel(): VPLinkModel | null {
          return new VPLinkModel();
      }

      canLinkToPort(port: PortModel): boolean {
        return port instanceof VPPortModel;
      }
}
