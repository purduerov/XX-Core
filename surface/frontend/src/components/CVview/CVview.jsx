import React, { Component } from 'react';
import styles from "./CVview.css";

export default class CVview extends Component {

    constructor(props) {
        super(props);

        this.test = false;
        this.ipAddressTest = "172.30.186.96";   //Charles hosting over competition wifi
        this.ipAddress = this.test?this.ipAddressTest:'localhost';   //Pakfront will be localhost:19[05, 27, etc]

        this.state = {cvClassPort: 1927, ipTail: "Need to fetch", Aircraft: "Need to fetch"};
        this.cpy = {cvClassPort: 1927, ipTail: "Need to fetch", Aircraft: "Need to fetch"};

        this.fetchStuff = this.fetchStuff.bind(this);
        this.checkPort = this.checkPort.bind(this);

        this.checkPort();

        this.fetchStuff();
    }

    fetchStuff() {
      $.ajax({
        dataType: 'json',
        url: 'http://localhost:1927/',
        success: (data) => {
          // console.log(data);
          try {
            this.cpy.Tail = data.Tail;
            this.cpy.Aircraft = data.Aircraft;

            this.setState(this.cpy);
          } catch(e) {
            console.log("Failed to get tail data");
          }
        },
        //timeout: 50,
        error: (data) => {
          console.log(data);
          console.log("An error occured on CVview");
          console.log('http://'+this.ipAddress+':'+this.state.cvClassPort+'/');
        }
      });
          //stuff = JSON.parse(success(data));
      setTimeout(this.fetchStuff, 55);
    }

    checkPort() {
      $.ajax({
        dataType: 'json',
        url: 'http://'+this.ipAddress+':1905/',//'http://'+this.ipAddress+':'+this.state.cvClassPort+'/',
        success: (data) => {
          //console.log(data);
          try {
            this.cpy.cvClassPort = data.cvTailClassify.data;

            this.setState(this.cpy);
          } catch (e) {
            console.log("Unsuccessful port find");
          }
        },
        //timeout: 500,
        error: (data) => {
          console.log(data);
          console.log("An error occured on CVview");
          console.log('http://'+this.ipAddress+':1927/');
        }
      });
    }

    render() {
        return (
        <div className={styles.container}>
            <div className={styles.tail}> Plane tail: {this.state.Tail} </div>
            <div className={styles.plane}> Plane class: {this.state.Aircraft} </div>
            <button onClick={this.checkPort}>Check Port</button>
        </div>
        );
    }
}
