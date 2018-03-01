These are the files that the driver interacts with.

An electron application runs our UI and webpage, which communicates back and forth with a Flask server on the RaspberryPi.

A gamepad library allows us to read a gamepad and interpret it into a desired vector of movement for the ROV.

Our compiler allows us to take all the desired components and merge them into 1 file of each type, for easy loading. This uses Reactjs, and a webpack/babel compiler to actually create the files to render.

`npm start` to run electron
`npm run dev` to build components in development (Which gives verbose error messages -- VERY useful)
`npm run watch` to set a watcher that will compile changed files automatically (in development mode) 
`npm run build` to build in production mode -- errors are links to their verbose counterparts to minimize space
