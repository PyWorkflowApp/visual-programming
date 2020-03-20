import { DefaultPortModel, NodeModel } from '@projectstorm/react-diagrams';

/**
 * Example of a custom model using pure javascript
 */
export class CustomNodeModel extends NodeModel {

    constructor(options = {}) {
        super({
            ...options,
            type: 'custom-node'
        });
        this.color = options.color || {
            options: 'red'
        };

        const nIn = options.numPortsIn === undefined ? 1 : options.numPortsIn;
        const nOut = options.numPortsOut === undefined ? 1 : options.numPortsOut;
        // setup in and out ports
        for (let i = 0; i < nIn; ++i) {
            this.addPort(
                new DefaultPortModel({
                    in: true,
                    type: 'in',
                    name: `in-${i}`
                })
            );
        }
        for (let i = 0; i < nOut; ++i) {
            this.addPort(
                new DefaultPortModel({
                    in: false,
                    type: 'out',
                    name: `out-${i}`
                })
            );
        }
    }

    serialize() {
        return {
            ...super.serialize(),
            color: this.options.color
        };
    }

    deserialize(ob, engine) {
        super.deserialize(ob, engine);
        this.color = ob.color;
    }
}
