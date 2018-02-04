# Pakfront Proxy
proxy that routes traffic between the frontend and ROV. Logs shit, passes image data to CV

## TODO
- transparent handling of flask requests+responses
- logging(and how we will log) functionallity for all processes

## Setup
run "npm install"
config file rules
Each process has an ID
to_client_video port = 4xID + 1917 + 1
to_client_data port  = 4xID + 1917 + 2
to_cv_process port   = 4xID + 1917 + 3 
to_cv_process_data   = 4xID + 1917 + 4
