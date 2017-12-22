import React from 'react';
import {render} from 'react-dom';
import Cam_view from './src/components/Cam_View.jsx';
import Titlebar from './src/components/Titlebar.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <Titlebar/>
        <Cam_view />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));
