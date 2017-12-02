import React from 'react';
import {render} from 'react-dom';
import Titlebar from './src/components/Titlebar.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
      <Titlebar/>
        <p> Hello React!</p>
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));
