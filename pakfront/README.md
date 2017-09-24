# Packfront Proxy
proxy that routes traffic between the frontend and ROV. Logs shit, passes image data to CV

## Setup

   Rasberry Pi                           Basestation
----------------                -------------------------------- 
|              |  http stream   |                              | 
|     Port 1917| -------------> |                              | 
|              |                |                              | 
|     ROV      |                |                              | 
|              |                |                              | 
|              |                |                              | 
----------------                -------------------------------- 
