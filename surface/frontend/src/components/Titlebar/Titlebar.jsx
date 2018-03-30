import React from 'react';
import styles from './titlebar.css';


//<img src={require('../assets/ieee.png')} />

class Titlebar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {text: "Purdue ROV 2018"};

    }

    render() {
        return (
            <div className={styles.title}>
                {this.state.text}
            </div>
        )
    }
}

export default Titlebar