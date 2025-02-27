A variety of Python based SaltStack Engines

## LoadBeaconEngine.py

This engine is used to capture the **salt/beacon/host-name-here/load/** events and process the data.
The data is written to two daily data files which are then available for third party tools to process.

 /data/self-heal/load/host-id-load-YYYY-MM-DD.log
 /data/self-heal/load/rector-YYYY-MM-DD.log

## DiskUsageBeaconEngine.py

This engine is used to capture the **salt/beacon/host-name-here/diskuage** events and process the data.
The data is written to two daily data files which are then available for third party tools to process.

 /data/self-heal/diskusage/host-id-diskusage-YYYY-MM-DD.log
 /data/self-heal/diskusage/rector-YYYY-MM-DD.log

 ## Configuring Saltstack

 To use the engines, create a file in /etc/salt/master.d/engines.conf and add the following (assuems you have no previous engines configured):

 ```
#
# Salt-Master will read /etc/salt/master.d for config files.
#
engines:
  - LoadBeaconEngine
  - DiskUsageBeaconEngine
```
Once created, restart your salt-master. **systemctl restart salt-master**

If you suspect issues, tail the master log file in **/var/log/salt/master**
