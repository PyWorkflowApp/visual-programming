import { DefaultLinkModel } from '@projectstorm/react-diagrams';

/**
 * Example of a custom model using pure javascript
 */
export class CustomLinkModel extends DefaultLinkModel {
      constructor() {
        super({
          type: 'advanced',
          width: 100
        });
      }
}
