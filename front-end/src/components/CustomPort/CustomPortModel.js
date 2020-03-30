import { DefaultPortModel } from '@projectstorm/react-diagrams';
import { CustomLinkModel } from '../CustomLink/CustomLinkModel';

export class CustomPortModel extends DefaultPortModel {
      createLinkModel() {
          return new CustomLinkModel();
      }

      canLinkToPort(port) {
        return port instanceof CustomPortModel;
      }
}
