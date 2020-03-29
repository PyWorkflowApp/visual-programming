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
}
