import React,{Component} from 'react';

import {variables} from '../Variables.js';
import Curator from './Curator.js'

export default class CuratorHolder extends Component{

    constructor(props){
        super(props);

        this.state={
            curators: []
        }
    }

    updateState() {
        fetch(variables.API_URL+'curators')
        .then(response=>response.json())
        .then(data=>{
            this.setState({curators:data});
        });
    }

    componentDidMount(){
        this.updateState();
    }

    render(){
        const {
            curators
        }=this.state;
        return(
            <div className="curator-holder">
                {curators.map(curator=>
                    <Curator id={curator.id} type={curator.type}/>
                )}
            </div>
        )
    }
}
