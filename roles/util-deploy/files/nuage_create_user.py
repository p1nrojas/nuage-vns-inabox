#!/usr/bin/python

from vspk import v4_0 as vspk
import argparse

def setup_logging():
   import logging
   from vspk.utils import set_log_level
   set_log_level(logging.DEBUG, logging.StreamHandler())

def start_csproot_session():
   session = vspk.NUVSDSession(
       username=args.cspuser,
       password=args.passwd,
       enterprise=args.org,
       api_url="https://%s:8443" % args.vsd_ip)
   try:
       session.start()
   except:
       logging.error('Failed to start the session')
   return session

parser = argparse.ArgumentParser()
parser.add_argument('cspuser', type=str)
parser.add_argument('passwd', type=str)
parser.add_argument('org', type=str)
parser.add_argument('vsd_ip', type=str)
parser.add_argument('new_user', type=str)
parser.add_argument('new_passwd', type=str)
parser.add_argument('email', type=str)
args =  parser.parse_args()

csp_session = start_csproot_session()

try:
   cspenterprise = vspk.NUEnterprise()
   cspenterprise.id = csp_session.me.enterprise_id
   csp_users = cspenterprise.users.get()
   lst_users = [usr.user_name for usr in csp_users]
   if args.new_user not in lst_users:
#       print 'INFO: Creating new user', args.new_user
       my_user = vspk.NUUser(first_name=args.new_user, last_name=args.new_user,
                             user_name=args.new_user, password=args.new_passwd, email=args.email)
       cspenterprise.create_child(my_user)
   else:
#       print 'INFO: New user', args.new_user, 'is already created'
       my_user = cspenterprise.users.get_first(filter="userName=='%s'" % args.new_user)

   #when you assign a user to a group, it will remove the old users from the group
   # a workaround is get the append function before the assign function
   csprootuser = vspk.NUUser(id=csp_session.me.id)
   csprootgroup = cspenterprise.groups.get_first(filter="name=='Root Group'")
   root_users = csprootgroup.users.get()
   lst_rootusersnames = [usrgroup.user_name for usrgroup in root_users]
   if args.new_user not in lst_rootusersnames:
#       print 'INFO: Assign new user', args.new_user, 'to group root'
       root_users.append(my_user)
       csprootgroup.assign(root_users, vspk.NUUser)
#
#   else:
#       print 'INFO: New user', args.new_user, 'is already assigned to group root'

   print "success"

except Exception as e:
   msg = "Exception is:\n %s \n" % e
   print msg

