import React,{Component} from 'react';

import {variables} from '../Variables.js';

export default class CuratorState extends Component{

    constructor(props){
        super(props);

        this.state={
            state: {},
            curatorState: {},
            environmentState: {},
        }
    }

    updateState() {
        fetch(variables.API_URL+'state/'+this.props.id)
        .then(response=>response.json())
        .then(data=>{
            if (data.hasOwnProperty('state') && data.hasOwnProperty('curatorState') && data.hasOwnProperty('environmentState')) {
                this.setState({state:data.state, curatorState:data.curatorState, environmentState:data.environmentState});
            } else {
                console.log('error in data: ', data);
            }
        })
        .catch(error => { 
            console.log('error', error);
            clearInterval(this.interval);
        });
    }

    renderState(state) {
        if (state !== null) {
            return (
                <div>
                    state: {state.data}
                </div>
            )
        } 
    }
    renderEnvState(environmentState) {
        if (environmentState !== null) {
            return (
                <div className='curator-state'>
                    environment state: {environmentState.accident}
                </div>
            )
        } 
    }
    renderCuratorState(curatorState) {
        if (this.props.type === 'AccessCurator') {
            return (
                <div className='curator-state'>
                    access: {this.renderAccess(curatorState.access)} <br/>
                    emergency exits: {String(curatorState.emergency_exits)} <br/>
                </div>
            )
        } else if (this.props.type === 'SecurityCurator') {
            return (
                <div className='curator-state'>
                    alert system: {String(curatorState.alert_system)} <br/>
                </div>
            )
        } else if (this.props.type === 'ResourceManagementCurator') {
            return (
                <div className='curator-state'> 
                    energy supply: {this.renderEnergySupply(curatorState.energy_supply)} <br/>
                    light: {String(curatorState.light)} <br/>
                    broken bulbs: {String(curatorState.broken_bulb_count)} of {String(curatorState.bulb_count)} (all bulbs are broken: {String(curatorState.all_bulbs_are_broken)}) <br/>
                    emergency lights: {String(curatorState.emergency_lights)}
                </div>
            )
        } else { }
    }
    renderAccess(access) {
        if (access === 0) {
            return (<>denied</>)
        } else if (access === 1) {
            return (<>restricted</>)
        } else {
            return (<>unlimited</>)
        }
    }
    renderEnergySupply(energy_supply) {
        if (energy_supply === 0) {
            return (<>switched off</>)
        } else if (energy_supply === 1) {
            return (<>switched on</>)
        } else {
            return (<>damaged</>)
        }
    }

    componentDidMount() {
        this.updateState()
        this.interval = setInterval(() => this.updateState(), variables.UPDATE_INTERVAL);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render(){
        const {
            state,
            curatorState,
            environmentState
        }=this.state;
        const {
            type,
            id,
        }=this.props;
        return(
            <div className='curator-info'>
                <div className='curator-info-row'>
                    <div className='curator-type'>[{id}] {type}</div>
                    {this.renderState(state)} 
                </div>
                <div className='curator-info-row'>
                    {this.renderEnvState(environmentState)} 
                    {this.renderCuratorState(curatorState)} 
                </div>
            </div>
        )
    }
}
