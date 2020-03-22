import { NodeModel } from '@projectstorm/react-diagrams';
import { CustomPortModel } from '../CustomPort/CustomPortModel';


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

        // user-defined description of node
        this._description = null;

        const nIn = options.numPortsIn === undefined ? 1 : options.numPortsIn;
        const nOut = options.numPortsOut === undefined ? 1 : options.numPortsOut;
        // setup in and out ports
        for (let i = 0; i < nIn; ++i) {
            this.addPort(
                new CustomPortModel({
                    in: true,
                    type: 'in',
                    name: `in-${i}`
                })
            );
        }
        for (let i = 0; i < nOut; ++i) {
            this.addPort(
                new CustomPortModel({
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

    getDescription() {
        return this._description;
    }

    setDescription(description) {
        this._description = description;
    }

}
