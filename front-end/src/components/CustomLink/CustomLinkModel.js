import { DefaultLinkModel } from '@projectstorm/react-diagrams';

export class CustomLinkModel extends DefaultLinkModel {
      constructor() {
        super({
          type: 'advanced',
          width: 5
        });
      }

    getSVGPath(): string {
  		if (this.isLastPositionDefault()) {
        return;
      }

		  return super.getSVGPath();
	}

  isLastPositionDefault() {
    return this.getLastPoint().getX() === 0 && this.getLastPoint().getY() === 0;
  }
}
