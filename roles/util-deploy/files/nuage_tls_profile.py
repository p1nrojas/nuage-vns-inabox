import pexpect
import time
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('vsc_host', type=str)
parser.add_argument('vsc_ip', type=str)
parser.add_argument('passwd', type=str)
parser.add_argument('cert_name', type=str)
args =  parser.parse_args()

try:
  child = pexpect.spawn('ssh admin@%s' % args.vsc_ip)
#  child.logfile = sys.stdout  # uncomment to debug
  child.expect ('password:')
  child.sendline (args.passwd)
  child.expect (args.vsc_host)
  child.sendline ('configure system security tls-profile "ex-tls-profile" create')
  child.expect (args.vsc_host)
  child.sendline (r'own-key "cf1:\%s-Key.pem"' % args.cert_name)
  child.expect (args.vsc_host)
  child.sendline (r'own-certificate "cf1:\%s.pem"' % args.cert_name)
  child.expect (args.vsc_host)
  child.sendline (r'ca-certificate "cf1:\%s-CA.pem"' % args.cert_name)
  child.expect (args.vsc_host)
  child.sendline ('no shutdown')
  child.expect (args.vsc_host)
  child.sendline ('exit all')
  child.expect (args.vsc_host)
  child.sendline ('configure vswitch-controller open-flow tls-profile "ex-tls-profile"')
  child.expect (args.vsc_host)
  child.sendline ('configure vswitch-controller xmpp tls-profile "ex-tls-profile"')
  child.expect (args.vsc_host)
  child.sendline ('admin save')
  child.expect (args.vsc_host)
  child.sendline ('logout')
  print "success"

except Exception as e:
   msg = "Exception is:\n %s \n" % e
   print msg 
