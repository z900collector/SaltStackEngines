"""
Capture Beacon Disk Usage Events

Save To: /data/self-heal/diskusage/<id>-load-YYYY-MM-DD.log
Format:  2025-01-03|15:31:03|/home|97.3

AND

Save to: /data/self-heal/diskusage/reactor-2024-12-26.log
Format: 2024-12-26|23:59:59|DISK|tri-xfer-to-isilon.int.tri.edu.au|/home|97.3
"""

import logging

import salt.returners
import salt.utils.files
import salt.utils.event
import salt.utils.json
import salt.client
import salt.config
import datetime
import time
import os

log = logging.getLogger(__name__)


def make_dir(newpath):
   """
   If path does not exist then it's created.
   """
   if not os.path.exists(newpath):
      os.makedirs(newpath)
   return





def event_bus_context(opts):
    if opts["__role"] == "master":
       event_bus = salt.utils.event.get_master_event(opts,opts["sock_dir"], listen=True)
    else:
       event_bus = salt.utils.event.get_event( "minion", opts=opts, sock_dir=opts["sock_dir"], listen=True,)
    return event_bus



def write_diskusage_data(id,mount,diskusage):
   today = time.strftime("%Y-%m-%d")
   now = time.strftime("%H:%M:%S")

# WR -> /data/self-heal/diskusage/<host-id>-diskusage-YYYY-MM-DD.log
# WR -> /data/self-heal/diskusage/reactor-YYYY-MM-DD.log

   reactor_log_file = "reactor-{0}.log".format(today)
   host_log_file = "{0}-load-{1}.log".format(id,today)

   datadir="/data/self-heal/diskusage/"
   make_dir(datadir)

   txt = "{0}|{1}|DISKUSAGE|{2}|{3}|{4}\n".format(today,now,id,mount,diskusage)
   target = datadir+reactor_log_file
   try:
      with salt.utils.files.flopen(target, "a") as lf1:
         lf1.write(txt)
   except Exception:
      log.error("LogFile 1 - write to log failed")
      raise

   txt = "{0}|{1}|{2}|{3}\n".format(today,now,mount,diskusage)
   target = datadir+host_log_file
   try:
      with salt.utils.files.flopen(target, "a") as lf2:
         lf2.write(txt)
   except Exception:
      log.error("LogFile 2 - write to log failed")
      raise
   return


def start():
    """
    Listen to Beacon events and write Diskusage events to data files as needed
    """
    log.debug("start() - ENTRY")
    with event_bus_context(__opts__) as event_bus:
       while True:
          event = event_bus.get_event(wait=10,tag="salt/beacon/", full=True)
          if event:
             jevent = salt.utils.json.dumps(event)
             id = event.get("id", "")
             diskusage = event.get("diskusage", "")
             if diskusage != "":
                mount = event.get("mount","")
                write_diskusage_data(id,mount,diskusage)
    log.debug("start() - EXIT")
#
# End of File
