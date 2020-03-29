import { NodeModel } from '@projectstorm/react-diagrams';
import { VPPortModel } from '../VPPort/VPPortModel';

export class CustomNodeModel extends NodeModel {

    constructor(options = {}) {
        super({
            ...options,
            type: 'custom-node'
        });

        // user-defined description of node
        this._description = null;

        const nIn = options.num_in === undefined ? 1 : options.num_in;
        const nOut = options.num_out === undefined ? 1 : options.num_out;
        // setup in and out ports
        for (let i = 0; i < nIn; ++i) {
            this.addPort(
                new VPPortModel({
                    in: true,
                    type: 'vp-port',
                    name: `in-${i}`
                })
            );
        }
        for (let i = 0; i < nOut; ++i) {
            this.addPort(
                new VPPortModel({
                    in: false,
                    type: 'vp-port',
                    name: `out-${i}`
                })
            );
        }
    }

    serialize() {
        return {
            ...super.serialize(),
            options: this.options,
        }
    }

    deserialize(ob, engine) {
        super.deserialize(ob, engine);
    }

    getDescription() {
        return this._description;
    }

    setDescription(description) {
        this._description = description;
    }

}
