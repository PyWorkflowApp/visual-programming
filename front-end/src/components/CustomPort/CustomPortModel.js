import { DefaultPortModel } from '@projectstorm/react-diagrams';
// import { CustomLinkModel } from '../CustomLink/CustomLinkModel';
import { DefaultLinkModel } from '@projectstorm/react-diagrams';


export class CustomPortModel extends DefaultPortModel {
      createLinkModel(): DefaultLinkModel | null {
          return new DefaultLinkModel();
      }

      canLinkToPort(port: PortModel): boolean {
        return port instanceof CustomPortModel;
      }
}
