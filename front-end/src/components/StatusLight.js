import React from 'react';
import * as _ from 'lodash';
import '../styles/StatusLight.css';


function StatusLight(props) {
    const statuses = {
        "unconfigured": "red",
        "configured": "yellow",
        "complete": "green"
    };
    const items = _.keys(statuses).map(s =>
        <StatusLightItem color={statuses[s]} active={props.status === s} key={s} />
    );
    return (
        <div className="StatusLight">
            { items }
        </div>
    )
}


function StatusLightItem(props) {
    const color = props.active ? props.color : "white";
    return (
        <div className="StatusLightItem" style={{backgroundColor: color}} />
    )
}


export default StatusLight;
