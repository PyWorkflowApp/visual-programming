import { DefaultPortModel } from '@projectstorm/react-diagrams';
import { CustomLinkModel } from '../CustomLink/CustomLinkModel';

export class CustomPortModel extends DefaultPortModel {
      createLinkModel(): CustomLinkModel | null {
          return new CustomLinkModel();
      }

      canLinkToPort(port: PortModel): boolean {
        return port instanceof CustomPortModel;
      }
}
