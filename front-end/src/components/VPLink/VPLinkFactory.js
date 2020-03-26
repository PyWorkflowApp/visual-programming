import * as React from 'react';
import { VPLinkModel } from './VPLinkModel';
import { VPLinkWidget } from './VPLinkWidget';
import { DefaultLinkFactory } from '@projectstorm/react-diagrams';

export class VPLinkFactory extends DefaultLinkFactory {

    generateModel(): VPLinkModel {
      return new VPLinkModel();
    }

    generateReactWidget(event): JSX.Element {
  		return <VPLinkWidget link={event.model} diagramEngine={this.engine} />;
  	}
}
