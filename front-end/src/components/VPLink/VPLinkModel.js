import { DefaultLinkModel } from '@projectstorm/react-diagrams';

export class VPLinkModel extends DefaultLinkModel {
    constructor() {
        super({
          type: 'default',
          width: 5,
          color: 'orange'
        });
    }

    getSVGPath() {
      if (this.isLastPositionDefault()) {
        return;
      }

      return super.getSVGPath();
    }

    isLastPositionDefault() {
      return this.getLastPoint().getX() === 0 && this.getLastPoint().getY() === 0;
    }

    /**
     * TODO: Notify backend the link has been removed
    */
    remove() {
      const sourcePort = this.getSourcePort(); // PortModel
      const sourceNode = sourcePort.getNode(); // NodeModel
      const targetPort = this.getTargetPort(); // PortModel
      const targetNode = targetPort.getNode(); // NodeModel
      
      super.remove();
    }
}
