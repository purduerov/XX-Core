# Auxillery Microcontrollers
This is the folder for the code for the microcontrollers that are interspersed around the rov. They are the transmitters, recievers and whatnot.

## Programming an Attiny with a Arduino
Wiring

| Arduino  | Attiny |
| -------- |:------:|
| Gnd      |6       |
| 11       | 11     |
| 5V       | 2      |
| 10       | 5      |
| 13       | 3      |
| 12       | 1      |
1. Upload the ArduinoISP onto the programming board
2. If the Attiny is not an available board, then go to File -> Preferances, and then select the window to the far right of the Additional Boards Manager URL box
3. In the popup, click "Unofficial Boards URLs". In the website that pops up, find Attiny, and copy the link associated with the attiny24
4. Paste the link into the "Enter Additional URLs", press ok
5. Go to Tools -> Board -> Boards Manager, select Attiny extra boards, click, then install
6. Go to tools ->board and choose Attiny24/44/84
7. In Tools -> micro choose Attiny 24 @ 16Mhz
8. In Tools -> Programmer choose "Arduinos as ISP"
9. In Tools -> Programmer, press "Burn Bootloader"
10. If you are on linux, you may need to run "sudo ln -s /lib/x86_64-linux-gnu/libreadline.so.7.0 /lib/x86_64-linux-gnu/libreadline.so.6" to link the readlines shared object they want
11. Upload as needed
