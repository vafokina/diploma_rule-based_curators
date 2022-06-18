import React,{Component} from 'react';

import {variables} from '../Variables.js';

export default class ControlPanel extends Component{

    sendEvent(factName, param) {
        var fact = {}
        if (factName === 'Fire') {
            fact = {
                "0": param
            }
        } else if (factName === 'Access') {
            fact = {
                "admission": param
            }
        } else if (factName === 'Violation') {
            fact = {}
        } else if (factName === 'Motion') {
            fact = {
                "0": param
            }
        } else if (factName === 'BrokenBulb') {
            fact = {}
        } else if (factName === 'BrokenEnergySupply') {
            fact = {}
        }

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
        "factName": factName,
        "fact": fact
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch(variables.API_URL+"event", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
    }

    sendGenerate(value) {
        fetch(variables.API_URL+'event?generate='+String(value),{
            method:'GET',
        })
    }

    render(){
        return(
            <div className="control-panel">
                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn btn-danger" onClick={()=>this.sendEvent("Fire", true)}>
                        Fire(true)
                    </button>
                    <button type="button" className="control-panel-btn btn btn-danger" onClick={()=>this.sendEvent("Fire", false)}>
                        Fire(false)
                    </button>
                </div>

                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("Access", true)}>
                        Access(true)
                    </button>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("Access", false)}>
                        Access(false)
                    </button>
                </div>
                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("Violation", true)}>
                        Violation()
                    </button>
                </div>

                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("Motion", true)}>
                        Motion(true)
                    </button>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("Motion", false)}>
                        Motion(false)
                    </button>
                </div>
                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("BrokenBulb")}>
                        BrokenBulb()
                    </button>
                </div>
                <div className='control-panel-column'>
                    <button type="button" className="control-panel-btn btn col-secondary" onClick={()=>this.sendEvent("BrokenEnergySupply")}>
                        BrokenEnergySupply()
                    </button>
                </div>
                <div className='control-panel-column right'>
                    <button type="button" className="control-panel-btn btn btn-success" onClick={()=>this.sendGenerate(true)}>
                        Generate(true)
                    </button>
                    <button type="button" className="control-panel-btn btn btn-success" onClick={()=>this.sendGenerate(false)}>
                        Generate(false)
                    </button>
                </div>
            </div>
        )
    }
}
