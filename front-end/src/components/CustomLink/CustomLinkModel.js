import { BezierCurve } from '@projectstorm/geometry';
import { DefaultLinkModel } from '@projectstorm/react-diagrams';

/**
 * Example of a custom model using pure javascript
 */
export class CustomLinkModel extends DefaultLinkModel {
      constructor() {
        super({
          type: 'advanced',
          width: 5
        });
      }

    getSVGPath(): string {
  		if (this.points.length !== 2 || this.isLastPositionDefault()) {
        return;
      }

			const curve = new BezierCurve();
			curve.setSource(this.getFirstPoint().getPosition());
			curve.setTarget(this.getLastPoint().getPosition());
			curve.setSourceControl(
				this.getFirstPoint()
					.getPosition()
					.clone()
			);
			curve.setTargetControl(
				this.getLastPoint()
					.getPosition()
					.clone()
			);

			if (this.sourcePort) {
				curve.getSourceControl().translate(...this.calculateControlOffset(this.getSourcePort()));
			}

			if (this.targetPort) {
        curve.getTargetControl().translate(...this.calculateControlOffset(this.getTargetPort()));
			}

			return curve.getSVGCurve();
	}

  isLastPositionDefault() {
    return this.getLastPoint().getX() === 0 && this.getLastPoint().getY() === 0;
  }
}
