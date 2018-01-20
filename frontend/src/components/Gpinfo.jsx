import React, { Component } from 'react';
import styles from "./Gp.info.css";

<div id="Gamepad">
    <h1>Gamepad</h1>
    <hr>
    <div class="gamepad">
      <ul v-for="(value, key) in data.buttons">
          <li>{{key}}: {{value}}</li>
      </ul>
      <hr>
      <p>left:</p>
      <div class="gp_axis">
        <ul v-for="(value, key) in data.axes.left">
            <li>{{key}}: {{value}}</li>
        </ul>
      </div>
      <hr>
      <p>right:</p>
      <div class="gp_axis">
        <ul v-for="(value, key) in data.axes.right">
            <li>{{key}}: {{value}}</li>
        </ul>
      </div>
    </div>
</div>

<script>
    export default {
        props: ['data']
    }
</script>
