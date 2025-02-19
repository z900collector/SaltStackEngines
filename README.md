A variety of Python based SaltStack Engines

## LoadBeaconEngine.py

This engine is used to capture the **salt/beacon/host-name-here/load/** events and process the data.
The data is written to two daily data files which are then available for third party tools to process.

 /data/self-heal/load/<host-id>-load-YYYY-MM-DD.log
 /data/self-heal/load/rector-YYYY-MM-DD.log

##
