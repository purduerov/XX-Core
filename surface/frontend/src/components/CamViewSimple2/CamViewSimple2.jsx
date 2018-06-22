import React, { Component } from 'react';
import styles from "./CamViewSimple2.css";
const { ipcRenderer } = window.require('electron');

export default class CamViewSimple extends Component {

    constructor(props) {
        super(props);

        this.test = false;
        this.ipAddressTest = "192.168.43.176";   //Charles hosting over competition wifi
        this.ipAddress = this.test?this.ipAddressTest:'localhost';   //Pakfront will be localhost:19[05, 27, etc]

        this.state = {cvCams: {"CVsimulate":{"data":1923,"stream":1922}, "cvDistanceMeasure":{"data":1931,"stream":1930}, "cvTailClassify":{"data":1927,"stream":1926}},
                      normCams: {"data": 5,"stream":8000},
                      feed: 8000
                    };
        this.cpy = $.extend(true, {}, this.state);

        this.checkProcesses = this.checkProcesses.bind(this);
        this.switchFeed = this.switchFeed.bind(this);
        //this.switchFeed = this.switchFeed.bind(this);
    }

    checkProcesses() {
      var data;
      $.ajax({
        dataType: 'json',
        url: 'http://'+this.ipAddress+':1905/',//'http://'+this.ipAddress+':'+this.state.cvClassPort+'/',
        success: (pakfrontInfo) => {
          data = pakfrontInfo;
        },
        error: () => {
          data = {"CVsimulate":{"data":1923,"stream":1922},"camnum0":{"data":-1,"stream":8000},"cvDistanceMeasure":{"data":1931,"stream":1930},"cvTailClassify":{"data":1927,"stream":1926},"metacams":{"numcams":0,"pakfront":5001,"rovdirect":5000},"socketio":{"numcams":0,"pakfront":5001,"rovdirect":5000}};
        },
        timeout: 500
      });
      //console.log(data);
      try {
        Object.keys(data).forEach((val, i) => {
          if(val.toLowerCase().startsWith("cv")) {
            this.cpy.cvCams[val] = data[val];
          }
        });
        this.cpy.normCams = data.metacams;

        this.setState(this.cpy);
      } catch (e) {
        console.log("Unsuccessful port find");
      }
    }

    switchFeed(e) {
      var last = this.state.feed;
      this.cpy.feed = this.state.normCams.stream + Number($(e.currentTarget).text().slice(-1));

      ipcRenderer.send('camera-send', {new: this.cpy.feed});

      this.setState(this.cpy);
    }

    rendButtons() {
      var buttons = [];
      for(var i = 0; i < this.state.normCams.data; i++) {
        buttons.push("cam"+i)
      }
      return (
        buttons.map((val, i) => {
          return <button onClick={this.switchFeed} className={styles.btn} key={val}>{val}</button>
        })
      )
    }

    render() {
        return (
        <div className={styles.container}>
            <div className={styles.camView}>
              <img width="100%" src={"http://"+this.ipAddress+":"+this.state.feed+"/"} />
            </div>
            <div className={styles.modeSelect}>
              <div className={styles.buttonSelect}>
                {this.rendButtons()}
              </div>
            </div>
        </div>
        );
    }

    componentDidMount() {
      this.checkProcesses();
    }
}
