import React, { Component } from 'react';
import styles from "./CamViewSimple.css";

export default class CamViewSimple extends Component {

    constructor(props) {
        super(props);

        this.test = false;
        this.ipAddressTest = "172.30.186.96";   //Charles hosting over competition wifi
        this.ipAddress = this.test?this.ipAddressTest:'localhost';   //Pakfront will be localhost:19[05, 27, etc]

        this.state = {cvCams: {"CVsimulate":{"data":1923,"stream":1922}, "cvDistanceMeasure":{"data":1931,"stream":1930}, "cvTailClassify":{"data":1927,"stream":1926}},
                      normCams: {"data":5,"stream":8000},
                      feed: 8000
                    };
        this.cpy = {cvCams: {"CVsimulate":{"data":1923,"stream":1922}, "cvDistanceMeasure":{"data":1931,"stream":1930}, "cvTailClassify":{"data":1927,"stream":1926}},
                    normCams: {"data":5,"stream":8000},
                    feed: 8000
                    };

        this.fetchStuff = this.fetchStuff.bind(this);
        this.checkProcesses = this.checkProcesses.bind(this);
        //this.switchFeed = this.switchFeed.bind(this);
    }


      /* fetch('http://localhost:1905', {
        method: "GET",
        //body: JSON.parse(data),
        headers: {"Content-Type": "application/json"},
        credentials: "same-origin" //not sure is necessary
      }).then(function(response) {
        data = JSON.parse(response);
        console.log(data);
        //assign parsed values as ports to listen to for functions underneath
      }, function(error) {
        //error message
      }) */

    fetchStuff() {
      $.ajax({
        dataType: 'json',
        url: 'http://'+this.ipAddress+':'+this.state.cvClassPort+'/',//'http://'+this.ipAddress+':'+this.state.cvClassPort+'/',
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
        error: (data) => {
          console.log(data);
          console.log("An error occured on CVview");
          http://172.30.186.96:1927/
          console.log('http://'+this.ipAddress+':'+this.state.cvClassPort+'/');
        }
      });
          //stuff = JSON.parse(success(data));
    }

    checkProcesses() {
      var data = {"CVsimulate":{"data":1923,"stream":1922},"camnum0":{"data":-1,"stream":8000},"cvDistanceMeasure":{"data":1931,"stream":1930},"cvTailClassify":{"data":1927,"stream":1926},"metacams":{"numcams":0,"pakfront":5001,"rovdirect":5000},"socketio":{"numcams":0,"pakfront":5001,"rovdirect":5000}};
      //console.log(data);
      try {
        Object.keys(data).forEach((val, i) => {
          console.log(val, i);
        });
        this.cpy.cvCams = data.metacams;

        this.setState(this.cpy);
      } catch (e) {
        console.log("Unsuccessful port find");
      }
      /*
      $.ajax({
        dataType: 'json',
        url: 'http://'+this.ipAddress+':1905/',//'http://'+this.ipAddress+':'+this.state.cvClassPort+'/',
        success: (data) => {
          data = {"CVsimulate":{"data":1923,"stream":1922},"camnum0":{"data":-1,"stream":8000},"cvDistanceMeasure":{"data":1931,"stream":1930},"cvTailClassify":{"data":1927,"stream":1926},"metacams":{"numcams":0,"pakfront":5001,"rovdirect":5000},"socketio":{"numcams":0,"pakfront":5001,"rovdirect":5000}};
          //console.log(data);
          try {
            Object.keys(data).forEach((val, i) => {
              console.log(val, i);
            }
            this.cpy.cvCams = data.metacams;

            this.setState(this.cpy);
          } catch (e) {
            console.log("Unsuccessful port find");
          }
        },
        //timeout: 500,
        error: (data) => {
          console.log(data);
          console.log("An error occured on CVview");
          http://172.30.186.96:1927/
          console.log('http://'+this.ipAddress+':1927/');
        }
      });
      */
    }

    switchFeed(e) {
      this.cpy.feed = $(e.currentTarget).text().slice(-1);

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

    componentDidMount() {
      this.checkProcesses();
    }

    render() {
        return (
        <div className={styles.container}>
            <div className={styles.camView}></div>
            <div className={styles.modeSelect}>
              <div className={styles.buttonSelect}>
                {this.rendButtons()}
              </div>
            </div>
        </div>
        );
    }
}
