import { NodeModel } from '@projectstorm/react-diagrams';
import { VPPortModel } from '../VPPort/VPPortModel';

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

        const nIn = options.num_in === undefined ? 1 : options.num_in;
        const nOut = options.num_out === undefined ? 1 : options.num_out;
        // setup in and out ports
        for (let i = 0; i < nIn; ++i) {
            this.addPort(
                new VPPortModel({
                    in: true,
                    type: 'in',
                    name: `in-${i}`
                })
            );
        }
        for (let i = 0; i < nOut; ++i) {
            this.addPort(
                new VPPortModel({
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
