import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import Card from './src/components/Card.jsx';
import Cam_view from './src/components/Cam_View.jsx';
import Titlebar from './src/components/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo.jsx';

class App extends React.Component {
  render () {
    return (
      <div className="main">
          <div className="titlebar">
          <Titlebar/>
          </div>
          <div className="main-container">
              <div className="camera-width full-height center">
              </div>
              <div className="data-width full-height">
                  <div className="data-column">
                  </div>
                  <div className="data-column">
                    <Card title="Thrusters">
                      <ThrusterInfo/>
                    </Card>
                  </div>
                  <div className="data-column">
                  </div>
              </div>
          </div>
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));