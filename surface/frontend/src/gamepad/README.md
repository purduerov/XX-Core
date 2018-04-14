*Insert something descriptive here*
The gamepad file uses the inputs from Chrome drivers which read a physical gamepad and processes them into a dynamic object called `gp` with fields for buttons and axis.        
Select controllers cycles through the options and locks on to the first familiar id after a button has been pressed (don't press a button on the controller that won't be used).
Map creates the dynamic object for the buttons and stores the address of the gamepad in variables used throughout the program. It compares the address of the gamepad to known IDs in betterlayouts, and uses the frameworks of the matching ID.
Update is the updating function, checking to see the value of each button/axis, and it checks to see if the axis have changed by 10% to account for the tiny amounts of change from true (0,0) that is present in all joysticks.
pressRelease takes the current value of buttons and compares them to their last values to determine if they have just been pressed or released in case people decide they want that functionality to do something.
Zero takes the difference from true (0,0) in the axis and makes them the new zero.
Adjust scales the values on the axis to be what we want, since the new zero isn't true zero.
