from subprocess import Popen, PIPE 
import sys
import os
import json
import pygtk
pygtk.require('2.0')
import gtk

try:
  session = os.environ["BWSESSION"]
except KeyError:
  print "Error: please log in to bitwarden (using 'bw login') and set BWSESSION variable"
  exit()



cmd = ["bw", "list", "items", "--session", session]

p = Popen(cmd, stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate()

if not stderr:
  parsed = json.loads(stdout)
else:
  print stderr
  exit()

if sys.argv[1] == "list":
  print "Listing logins"
  for entry in parsed: print entry['name']
  exit()

requested_login = sys.argv[1]
print "Trying to find password for", requested_login


for entry in parsed:
  if requested_login in entry['name']:
    print "Found:", entry['name']

    pw = entry['login']['password']
    clipboard = gtk.clipboard_get()
    clipboard.set_text(pw)
    clipboard.store()
