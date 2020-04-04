import { DefaultLinkModel } from '@projectstorm/react-diagrams';
import * as API from '../../API';

export class VPLinkModel extends DefaultLinkModel {
    constructor() {
        super({
          type: 'default',
          width: 5,
          color: 'orange'
        });
        this.registerListener({
            targetPortChanged: event => {
                API.addEdge(this).catch(() => {});
            },
        })
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
        console.log("deleting link");
        API.deleteEdge(this)
            .then(() => super.remove())
            .catch(() => {});
    }
}
