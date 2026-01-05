import multiprocessing
from autodelete import autodeleteloop
from os import environ

wsgi_app = "main:app"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 1500 # autorestart for performance
max_requests_jitter = 200

default_proc_name="MFTalk-server"
bind=f"0.0.0.0:{environ.get("SERVER_PORT")}"

# Restrict logging everything....
disable_redirect_access_to_syslog = True
access_log_format='RESTRICTED'


def when_ready(server):
    autodeleteloop()
    print("autodelete inizialised")
    VERSION = open("../VERSION").read()
    print(f"Welcome to MFTalk server (v.{VERSION}), starting/started {workers} workers")


def on_exit(server):
    print(f"stopping {default_proc_name}")