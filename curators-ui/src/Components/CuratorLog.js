import React,{Component} from 'react';

import {variables} from '../Variables.js';

export default class CuratorLog extends Component{

    constructor(props){
        super(props);

        this.state={
            log: ""
        }
    }

    updateState() {
        fetch(variables.API_URL+'log/'+this.props.id)
        .then(response=>response.json())
        .then(data=>{
            this.setState({log:data});
        })
        .catch(error => { 
            console.log('error', error);
            clearInterval(this.interval);
        });
    }

    componentDidMount() {
        this.updateState()
        this.interval = setInterval(() => this.updateState(), variables.UPDATE_INTERVAL);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render(){
        return(
            <div className="curator log-box">
                <div className="log-box-scroll">
                    <div className="log-text-box">
                        <pre> 
                            {this.state.log}
                        </pre>
                    </div>
                </div>
            </div>
        )
    }
}
