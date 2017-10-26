These are the files that the driver interacts with.

An electron application runs our UI and webpage, which communicates back and forth with a Flask server on the RaspberryPi.

A gamepad library allows us to read a gamepad and interpret it into a desired vector of movement for the ROV.

Our compiler allows us to take all the desired components and merge them into 1 file of each type, for easy loading.
