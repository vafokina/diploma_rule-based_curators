import './App.css';

import './Components/Log.css';
import './Components/Curator.css';
import './Components/ControlPanel.css';

import CuratorHolder from './Components/CuratorHolder.js'
import GeneralLog from './Components/GeneralLog.js'
import ControlPanel from './Components/ControlPanel.js'

function App() {
  return (
    <>
      <GeneralLog />      
      <CuratorHolder />
      <div className="control-panel-back" />
      <div className="fixed-footer border-top border-primary bg-light">
        <ControlPanel />
      </div>
    </>
  );
}

export default App;
