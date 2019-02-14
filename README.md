# CiscoUmbrella
Some scripts to automate the routine

## umbrella.py 
Query Umbrella using command promt.
Uses Umbrella reporting API

## Umbrella http error code 408
This error is undocumented on the Cisco's developers portal, so I guess it's important to mention it here. Almost every request usually ends with 408. You need to repeat it with same domain and same timstamp for a few minutes until you will get a result. All searches are cached on the server side for 10 minutes.  
