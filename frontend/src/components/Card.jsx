import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from "./Card.css";


export default class Card extends Component {

  constructor(props) {
    super(props);
    
  }

  render() {
      return (
        <div className={styles.container}>
            <div className={styles.card}>
                <div className={styles.mainContainer}>
                    <h1 className={styles.title}>{this.props.title}</h1>
                    <hr className={styles.squashed}/>
                    <div className={styles.inner}>
                        {this.props.children}
                    </div>
                </div>
            </div>
        </div>
      )
  }
}