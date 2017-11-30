import React from 'react';

class NewComponent extends React.Component {
   constructor() {
      super();

      this.state = {
         data: [
          "Me"
         ]
      }

      this.setStateHandler = this.setStateHandler.bind(this);
   };

   setStateHandler() {
      var item = "Me too..."
      var myArray = this.state.data;
      myArray.push(item)
      this.setState({data: myArray})
   };

   render() {
      return (
         <div>
            <button onClick = {this.setStateHandler}>SET STATE</button>
            <h4>State Array: {this.state.data}</h4>
         </div>
      );
   }
}

export default NewComponent;
