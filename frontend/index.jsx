import React from 'react';
import {render} from 'react-dom';
import AwesomeComponent from './src/components/AwesomeComponent.jsx';
import NewComponent from './src/components/NewComponent.jsx';

/*
class App extends React.Component {
  render () {
    return <p> Hello React, how do the do?!</p>;
  }
}
*/
class App extends React.Component {
  render () {
    return (
      <div>
        <p> Hello React!</p>
        <AwesomeComponent />
        <NewComponent />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));
