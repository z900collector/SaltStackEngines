"""
Capture Beacon Load Events

Saves beacon data To: /data/self-heal/load/<id>-load-YYYY-MM-DD.log
Format:  2025-01-03|15:31:03|0.11|0.06|0.09

AND

Save to: /data/self-heal/load/reactor-2024-12-26.log
Format: 2024-12-26|23:59:59|LOAD|tri-xfer-to-isilon.int.tri.edu.au|0.16|0.09|0.08
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


def write_load_data(id,m1,m5,m15):
   today = time.strftime("%Y-%m-%d")
   now = time.strftime("%H:%M:%S")

# WR -> /data/self-heal/load/<host-id>-load-YYYY-MM-DD.log
# WR -> /data/self-heal/load/rector-YYYY-MM-DD.log

   reactor_log_file = "reactor-{0}.log".format(today)
   host_log_file = "{0}-load-{1}.log".format(id,today)

   datadir="/data/self-heal/load/"
   make_dir(datadir)

   txt = "{0}|{1}|LOAD|{2}|{3}|{4}|{5}\n".format(today,now,id,m1,m5,m15)
   target = datadir+reactor_log_file
   try:
      with salt.utils.files.flopen(target, "a") as lf1:
         lf1.write(txt)
   except Exception:  # pylint: disable=broad-except
      log.error("LogFile 1 - write to log failed")
      raise

   txt = "{0}|{1}|{2}|{3}|{4}\n".format(today,now,m1,m5,m15)
   target = datadir+host_log_file
   try:
      with salt.utils.files.flopen(target, "a") as lf2:
         lf2.write(txt)
   except Exception:  # pylint: disable=broad-except
      log.error("LogFile 2 - write to log failed")
      raise
   return



def start():
    """
    Listen to Beacon events and write LOAD events to data files as needed
    """
    log.debug("start() - ENTRY")
    with event_bus_context(__opts__) as event_bus:
       while True:
#          log.warning("LOOP - event_bus.get_event()\n")
          event = event_bus.get_event(wait=10,tag="salt/beacon/")
          if event:
             jevent = salt.utils.json.dumps(event)
             id = event.get("id", "")
             m1 = event.get("1m", "")
             if m1 != "":
                m5 = event.get("5m","")
                m15 = event.get("15m","")
                write_load_data(id,m1,m5,m15)
    log.debug("start() - EXIT")
#
# End of File


