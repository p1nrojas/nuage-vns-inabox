#!/usr/bin/env python

# Created on 2017-2-13
# 
# @author: Mostafa Mostafa
# @copyright: Nokia 2017
# @version: 1.0.0
# 
# To run the script, you need to install vspk, just type:
#    pip install vspk
#
# To find new api calls, https://nuagenetworks.github.io/vspkdoc/html/quickstart.html
#
# Script Summary:
#     This script does the following:
#     1) Install License
#     2) Creates New users: "proxy user" & "vnsportal user", and add them to csp root group
#     3) Creates Infrastructure Gateway Profile
#     4) Creates Infrastructure VSC Profile
#     5) Creates Infrastructure Access Profile
#     6) Creates Infrastructure NSG Templates (3 templates)
#     7) Creates Organization Profile for the Enterprise
#     8) Enable VSS flow and event collection in the Infrastructure system config
#     9) Creates New Enterprise
#     10) Creates New Enterprise user: admin, and add it to the enterprise admin group
#     11) Creates Two Domain Templates: one encrypted and one not encrypted
#     12) Creates Branch (encrypted) Domain, 3 Zones, and 5 Subnets
#     13) Creates DC (non encrypted) Domain, 3 Zones, and 3 Subnets
#     14) Creates NSG instances from the NSG templates
#

############################################# 
# Parameters 
############################################# 

# Define Global Variables
vsd_ip = '10.31.134.242'
api_url = "https://10.31.134.242:8443"
username = "csproot"
password = "csproot"
enterprise = "csp"

# Variables for adding root Users and enterprise admin user
userName1 = "proxy"
userName2 = "vnsportal"
userEntName1 = "admin"
userEmail = "@mostafa.lab"

# CSPRoot VNS Infrastructure Gateway settings
infrGwName = 'GW_Profile_OneFactorAuth'
upgradeAction = 'UPGRADE_AT_BOOTSTRAPPING'
lab_fqdn = 'proxy1.mostafa.lab'

# CSPRoot VNS Infrastructure VSC settings
infrVsc1Name = 'vsc_245'
VSC1_IP = "10.31.134.245"
infrVsc2Name = 'vsc_246'
VSC2_IP = "10.31.134.246"

# CSPRoot VNS Infrastructure SSH Access settings
infrAccessName='Infra_Access_Profile'
infrAccessUserName='nuage'
infrAccessPassword='Alcateldc'
           
# CSPRoot VNS NSG Templates
nsgTemplate1Name = 'NSGV_1WAN_1LAN'
nsgTemplate2Name = 'NSGV_2WAN_2LAN'
nsgTemplate3Name = 'NSGE_2WAN_4LAN'

# Create NSG instances from the NSG templates
NSGName1="NSG-B1"
NSGName2="NSG-B2"
NSGName3="NSG-HQ"

# Variables for Organization Profile
infrOrganizationProfileName = 'Org_Profile'

# Variables for Enterprise/Domain templates
enterpriseName = "Enterprise1"
enterpriseLocalAS = "65001"
brdomainTemplate = "Branch_domain_template"
dcdomainTemplate = "DC_domain_template"
domainDNS = "10.31.134.255"

# Variables for Branch domain
brdomainName = "VPN_domain"
zone1Name = "Branch 1"
zone2Name = "Branch 2"
zone3Name = "HQ"
zone1Description = "San Jose"
zone2Description = "Los Angeles"
zone3Description = "Mountain View"
subnet1Name = "Data_Subnet_Br1"
subnet1IpAddr = "192.1.10.0"
subnet1Prefix = "255.255.255.0"
subnet1DhcpMinRange = "192.1.10.10"
subnet1DhcpMaxRange = "192.1.10.99"
subnet2Name = "Guest_Subnet_Br1"
subnet2IpAddr = "192.1.11.0"
subnet2Prefix = "255.255.255.0"
subnet2DhcpMinRange = "192.1.11.10"
subnet2DhcpMaxRange = "192.1.11.99"
subnet3Name = "Data_Subnet_Br2"
subnet3IpAddr = "192.1.20.0"
subnet3Prefix = "255.255.255.0"
subnet3DhcpMinRange = "192.1.20.10"
subnet3DhcpMaxRange = "192.1.20.99"
subnet4Name = "DMZ_Subnet_HQ"
subnet4IpAddr = "192.1.30.0"
subnet4Prefix = "255.255.255.0"
subnet4DhcpMinRange = "192.1.30.10"
subnet4DhcpMaxRange = "192.1.30.99"
subnet5Name = "Mgmt_Subnet_HQ"
subnet5IpAddr = "192.1.31.0"
subnet5Prefix = "255.255.255.0"
subnet5DhcpMinRange = "192.1.31.10"
subnet5DhcpMaxRange = "192.1.31.99"

# Variables for DC domain
dcdomainName = "DC_domain"
dczone1Name = "DataCenter"
dczone1Description = "Mountain View"
dcsubnet1Name = "VMs"
dcsubnet1IpAddr = "192.1.50.0"
dcsubnet1Prefix = "255.255.255.0"
dcsubnet1DhcpMinRange = "192.1.50.10"
dcsubnet1DhcpMaxRange = "192.1.50.99"
dcsubnet2Name = "Containers"
dcsubnet2IpAddr = "192.1.60.0"
dcsubnet2Prefix = "255.255.255.0"
dcsubnet2DhcpMinRange = "192.1.60.10"
dcsubnet2DhcpMaxRange = "192.1.60.99"
dcsubnet3Name = "Appliances"
dcsubnet3IpAddr = "192.1.70.0"
dcsubnet3Prefix = "255.255.255.0"
dcsubnet3DhcpMinRange = "192.1.70.10"
dcsubnet3DhcpMaxRange = "192.1.70.99"
dcsubnet4Name = "Bare_Metal_Servers"
dcsubnet4IpAddr = "192.1.80.0"
dcsubnet4Prefix = "255.255.255.0"
dcsubnet4DhcpMinRange = "192.1.80.10"
dcsubnet4DhcpMaxRange = "192.1.80.99"

# My standalone license - expires on june 2017
myLicense = """MDEyOIckSkDNYxvBMQ7R5Si0blD3By2oXRMBiv8JTWPLHCN3bQPaLLHHvlHblJwAjHZTRUHo3LA1Ky
hFX0YcTIQNEwDtvRpB5x0ZRw0SWIy/j6vFF5Faehtb7v9qmjQvOdNvNEa+MGk/JUljYfwyp/O4w9Hu
S2+pLFWXQPvK3DP2mC2aMDE2MjCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAkOyl181q5j2UHP
UCD5nzBE5Gz0g3N1n8KAs6aEcNO7ueXvPUeiuNQ//ui0vE9otuo4AnLJkLKuxoIJmVjIKzxXlMEqsA
K5zwOJpECOTEMxjZkyWcAujQg/ajVRcUAW+91UPz2nkzs1WkPhKs5ZjJTrksoEvmMt5fhNFXgLY2jC
cCAwEAATA3MzV7InByb3ZpZGVyIjoiTnVhZ2UgTmV0d29ya3MgLSBBbGNhdGVsLUx1Y2VudCBJbmMi
LCJwcm9kdWN0VmVyc2lvbiI6IjQuMCIsImxpY2Vuc2VJZCI6MSwibWFqb3JSZWxlYXNlIjoxLCJtaW
5vclJlbGVhc2UiOjAsInVzZXJOYW1lIjoiYWRtaW4iLCJlbWFpbCI6Im1vc3RhZmEubWFuc291ckBu
dWFnZW5ldHdvcmtzLm5ldCIsImNvbXBhbnkiOiJudWFnZSBkZW1vIiwicGhvbmUiOiIyMDIyMTU0NT
EwIiwic3RyZWV0IjoiNzU1IFJhdmVuZGFsZSBEciwgTW91bnRhaW4gVmlldywgQ0EgOTQwNDMgIiwi
Y2l0eSI6Im1vdW50YWluIHZpZXciLCJzdGF0ZSI6ImNhIiwiemlwIjoiOTQwNDMiLCJjb3VudHJ5Ij
oidXNhIiwiY3VzdG9tZXJLZXkiOiJmZWZlZmVmZS1mZWZlLWZlZmUtZmVmZSIsImFsbG93ZWRWTXND
b3VudCI6LTEsImFsbG93ZWROSUNzQ291bnQiOi0xLCJhbGxvd2VkVlJTc0NvdW50IjoyMCwiYWxsb3
dlZFZSU0dzQ291bnQiOjIwLCJhbGxvd2VkQ1BFc0NvdW50IjoyMCwiaXNDbHVzdGVyTGljZW5zZSI6
ZmFsc2UsImV4cGlyYXRpb25EYXRlIjoiNi8yNS8yMDE3IDEyOjAwOjAwIEFNIiwiZW5jcnlwdGlvbk
1vZGUiOnRydWUsImxpY2Vuc2VFbnRpdGllcyI6IntcImRlcGxveW1lbnRUeXBlXCI6XCJSbkRcIixc
ImxpY2Vuc2VSZXF1ZXN0SURcIjpcInJlcXVlc3QtMjEyMS5yZXFcIn0iLCJhZGRpdGlvbmFsU3VwcG
9ydGVkVmVyc2lvbnMiOiIwIiwibGljZW5zZWRGZWF0dXJlIjoiVlNTIn0="""


###########################################
# Initialize the VSD for a VNS deployment #
###########################################

from vspk import v4_0 as vspk
import pexpect             # python implementation of Expect
import time                # library needed for wait/sleep time functions
import sys                 # use sys exit function
#import argparse            # add options to the cli argument


###########################################
#  Create and Assign User to root group   #
###########################################
def func_create_users(session,userName,userEmail):
    cspenterprise = vspk.NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if userName not in lst_users:
        print 'INFO: Creating new user', userName
        my_user = vspk.NUUser(first_name=userName, last_name=userName, 
                              user_name=userName, password=userName, email=userName+userEmail)
        cspenterprise.create_child(my_user)
    else:
        print 'INFO: New user', userName, 'is already created'
        my_user = cspenterprise.users.get_first(filter="userName=='%s'" % userName) 

    #when you assign a user to a group, it will remove the old users from the group
    # a workaround is get the append function before the assign function
    csprootuser = vspk.NUUser(id=session.me.id)
    csprootgroup = cspenterprise.groups.get_first(filter="name=='Root Group'")
    root_users = csprootgroup.users.get()
    lst_rootusersnames = [usrgroup.user_name for usrgroup in root_users]
    if userName not in lst_rootusersnames:
        print 'INFO: Assign new user', userName, 'to group root'
        root_users.append(my_user)
        csprootgroup.assign(root_users, vspk.NUUser)

    else:
        print 'INFO: New user', userName, 'is already assigned to group root'


############################################# 
# create VNS infrastructure - NSG profile
############################################# 
def func_create_infr_gw_profiles(csprootSession):
    infra_gw_profile = csprootSession.infrastructure_gateway_profiles.get_first(filter="name == '%s'" % infrGwName)
    if not infra_gw_profile:
        print 'INFO: Creating Infrastructure Gateway Profile'
        metadata_path = 'http://%s/metadata.json' % lab_fqdn
        infra_gw_profile = vspk.NUInfrastructureGatewayProfile(name=infrGwName, 
            proxy_dns_name=lab_fqdn, system_sync_scheduler='0 0 * * *', 
            upgrade_action=upgradeAction, metadata_upgrade_path=metadata_path)
        csprootSession.create_child(infra_gw_profile)
    else:
        print 'INFO: Infrastructure Gateway Profile already created'
    return infra_gw_profile


############################################# 
# create VNS infrastructure - VSC profile
############################################# 
def func_create_infr_vsc_profiles(csprootSession,infrVscName,VSC_IP):
    infrastructure_vsc_profile = csprootSession.infrastructure_vsc_profiles.get_first(filter="name == '%s'" % infrVscName)
    if not infrastructure_vsc_profile:
        print 'INFO: Creating Infrastructure VSC:', infrVscName, ' Profile'
        infrastructure_vsc_profile = vspk.NUInfrastructureVscProfile(name=infrVscName, 
            first_controller=VSC_IP)
        csprootSession.create_child(infrastructure_vsc_profile)
    else:
        print 'INFO: Infrastructure VSC:', infrVscName, ' Profile already created'

    return infrastructure_vsc_profile


############################################# 
# create VNS infrastructure - Access profile
############################################# 
def func_create_infr_access_profiles(csprootSession,infrAccessName,infrAccessUserName,infrAccessPassword):
    f_infr_access_profile = csprootSession.infrastructure_access_profiles.get_first(filter="name == '%s'" % infrAccessName)
    if not f_infr_access_profile:
        print 'INFO: Creating Infrastructure Access Profile'
        f_infr_access_profile = vspk.NUInfrastructureAccessProfile(name=infrAccessName,user_name=infrAccessUserName,password=infrAccessPassword)
        csprootSession.create_child(f_infr_access_profile)
    else:
        print 'INFO: Infrastructure Access Profile already created'

    return f_infr_access_profile


######################################################
# Create NSG-E template (2 network, 4 access) 
######################################################
def func_create_nsg_2w_4l_template(csprootSession,nsgTemplateName,
                                infrastructure_gw_profile,infra_access_profile,
                                infrastructure_vsc_profile1,infrastructure_vsc_profile2):
    nsgateway_nsg = csprootSession.ns_gateway_templates.get_first(filter="name == '%s'" % nsgTemplateName)
    if not nsgateway_nsg:
        print 'INFO: Creating NSG-E Template (2 network, 4 access)',
        nsgateway_nsg = vspk.NUNSGatewayTemplate(name=nsgTemplateName, 
            description='Two Uplinks NSG-E', infrastructure_profile_id=infrastructure_gw_profile.id, 
            infrastructure_access_profile_id=infra_access_profile.id, personality='NSG', ssh_service='ENABLED', instance_ssh_override='ALLOWED')
        csprootSession.create_child(nsgateway_nsg)

        #Defining all ports
        p1 = vspk.NUNSPortTemplate(name='port1',port_type='NETWORK',physical_name='port1')
        p2 = vspk.NUNSPortTemplate(name='port2',port_type='NETWORK',physical_name='port2')
        p3 = vspk.NUNSPortTemplate(name='port3',port_type='ACCESS',physical_name='port3', vlan_range='0-4094')
        p4 = vspk.NUNSPortTemplate(name='port4',port_type='ACCESS',physical_name='port4', vlan_range='0-4094')
        p5 = vspk.NUNSPortTemplate(name='port5',port_type='ACCESS',physical_name='port5', vlan_range='0-4094')
        p6 = vspk.NUNSPortTemplate(name='port6',port_type='ACCESS',physical_name='port6', vlan_range='0-4094')

        #assigning ports to NSG-E template
        nsgateway_nsg.create_child(p1)
        nsgateway_nsg.create_child(p2)
        nsgateway_nsg.create_child(p3)
        nsgateway_nsg.create_child(p4)
        nsgateway_nsg.create_child(p5)
        nsgateway_nsg.create_child(p6)

        #creating and assigning VLAN 0 to network port
        uplink_vlan1 = vspk.NUVLANTemplate(value='0', associated_vsc_profile_id=infrastructure_vsc_profile1.id)
        p1.create_child(uplink_vlan1)

        uplink_vlan2 = vspk.NUVLANTemplate(value='0', associated_vsc_profile_id=infrastructure_vsc_profile2.id)
        p2.create_child(uplink_vlan2)
        
        #creating uplink connection type (DHCP/Primary/Secondary)
        primary_uplink_connection = vspk.NUUplinkConnection(mode='Dynamic', role='PRIMARY')
        uplink_vlan1.create_child(primary_uplink_connection)
        secondary_uplink_connection = vspk.NUUplinkConnection(mode='Dynamic', role='SECONDARY')
        uplink_vlan2.create_child(secondary_uplink_connection)

        #creating and assigning VLAN 0 to access port
        p_vlan = vspk.NUVLANTemplate(value='0')
        p3.create_child(p_vlan)
        p4.create_child(p_vlan)
        p5.create_child(p_vlan)
        p6.create_child(p_vlan)
        
    else:
        print ('INFO: NSG-E Template (2 network, 4 access) is already created')
    return nsgateway_nsg


######################################################
# NSG-V template (1 network, 1 access) 
######################################################
def func_create_nsg_1w_1l_template(csprootSession,nsgTemplateName,
                                infrastructure_gw_profile,infra_access_profile,
                                infrastructure_vsc_profile1,infrastructure_vsc_profile2):
    nsgateway_nsg = csprootSession.ns_gateway_templates.get_first(filter="name == '%s'" % nsgTemplateName)
    if not nsgateway_nsg:
        print 'INFO: Creating NSG-V Template (1 network, 1 access)'
        nsgateway_nsg = vspk.NUNSGatewayTemplate(name=nsgTemplateName, 
            description='One Uplinks NSG-V', infrastructure_profile_id=infrastructure_gw_profile.id, 
            infrastructure_access_profile_id=infra_access_profile.id, personality='NSG', ssh_service='ENABLED', instance_ssh_override='ALLOWED')
        csprootSession.create_child(nsgateway_nsg)

        #Defining all ports
        p1 = vspk.NUNSPortTemplate(name='port1',port_type='NETWORK',physical_name='port1')
        p2 = vspk.NUNSPortTemplate(name='port2',port_type='ACCESS',physical_name='port2', vlan_range='0-4094')

        #assigning ports to NSG-V template
        nsgateway_nsg.create_child(p1)
        nsgateway_nsg.create_child(p2)

        #creating and assigning VLAN 0 to network port
        uplink_vlan1 = vspk.NUVLANTemplate(value='0', associated_vsc_profile_id=infrastructure_vsc_profile1.id)
        p1.create_child(uplink_vlan1)
        
        #creating uplink connection type (DHCP/Primary/Secondary)
        primary_uplink_connection = vspk.NUUplinkConnection(mode='Dynamic', role='PRIMARY')
        uplink_vlan1.create_child(primary_uplink_connection)

        #creating and assigning VLAN 0 to access port
        p_vlan = vspk.NUVLANTemplate(value='0')
        p2.create_child(p_vlan)
        
    else:
        print ('INFO: NSG-V Template (1 network, 1 access) is already created')   
    return nsgateway_nsg
    

######################################################
# Create NSG-V template (2 network, 2 access) 
######################################################
def func_create_nsg_2w_2l_template(csprootSession,nsgTemplateName,
                                infrastructure_gw_profile,infra_access_profile,
                                infrastructure_vsc_profile1,infrastructure_vsc_profile2):
    nsgateway_nsg = csprootSession.ns_gateway_templates.get_first(filter="name == '%s'" % nsgTemplateName)
    if not nsgateway_nsg:
        print 'INFO: Creating NSG-V Template (2 network, 2 access)'
        nsgateway_nsg = vspk.NUNSGatewayTemplate(name=nsgTemplateName, 
            description='Two Uplinks NSG-V', infrastructure_profile_id=infrastructure_gw_profile.id, 
            infrastructure_access_profile_id=infra_access_profile.id, personality='NSG', ssh_service='ENABLED', instance_ssh_override='ALLOWED')
        csprootSession.create_child(nsgateway_nsg)

        #Defining all ports
        p1 = vspk.NUNSPortTemplate(name='port1',port_type='NETWORK',physical_name='port1')
        p2 = vspk.NUNSPortTemplate(name='port2',port_type='NETWORK',physical_name='port2')
        p3 = vspk.NUNSPortTemplate(name='port3',port_type='ACCESS',physical_name='port3', vlan_range='0-4094')
        p4 = vspk.NUNSPortTemplate(name='port4',port_type='ACCESS',physical_name='port4', vlan_range='0-4094')

        #assigning ports to NSG-V template
        nsgateway_nsg.create_child(p1)
        nsgateway_nsg.create_child(p2)
        nsgateway_nsg.create_child(p3)
        nsgateway_nsg.create_child(p4)

        #creating and assigning VLAN 0 to network port
        uplink_vlan1 = vspk.NUVLANTemplate(value='0', associated_vsc_profile_id=infrastructure_vsc_profile1.id)
        p1.create_child(uplink_vlan1)

        uplink_vlan2 = vspk.NUVLANTemplate(value='0', associated_vsc_profile_id=infrastructure_vsc_profile2.id)
        p2.create_child(uplink_vlan2)
        
        #creating uplink connection type (DHCP/Primary/Secondary)
        primary_uplink_connection = vspk.NUUplinkConnection(mode='Dynamic', role='PRIMARY')
        uplink_vlan1.create_child(primary_uplink_connection)
        secondary_uplink_connection = vspk.NUUplinkConnection(mode='Dynamic', role='SECONDARY')
        uplink_vlan2.create_child(secondary_uplink_connection)

        #creating and assigning VLAN 0 to access port
        p_vlan = vspk.NUVLANTemplate(value='0')
        p3.create_child(p_vlan)
        p4.create_child(p_vlan)

    else:
        print ('INFO: NSG-V Template (2 network, 2 access) is already created')
    return nsgateway_nsg


###########################################
# Creating New Organization Profile  #
###########################################
def func_create_infr_org_profiles(csprootSession,infrOrganizationProfileName):
    infrastructure_org_profile = csprootSession.enterprise_profiles.get_first(filter="name == '%s'" % infrOrganizationProfileName)
    if not infrastructure_org_profile:
        print 'INFO: Creating Organization Profile:', infrOrganizationProfileName
        infrastructure_org_profile = vspk.NUEnterpriseProfile(name=infrOrganizationProfileName, 
            allow_advanced_qos_configuration=True, allow_gateway_management=True, 
            allow_trusted_forwarding_class=True, 
            allowed_forwarding_classes=['A', 'B', 'C', 'D', 'E', 'F' ,'G', 'H'], 
            bgp_enabled=True, enable_application_performance_management=True, 
            encryption_management_mode='MANAGED')
        csprootSession.create_child(infrastructure_org_profile)
    else:
        print 'INFO: Organization Profile already created', infrOrganizationProfileName

    return infrastructure_org_profile


###########################################
# Enabling VSS Flow Collection            #
###########################################
def func_enable_vss_flow_collection(session):
    sysconfig = session.me.system_configs.get_first()
    if sysconfig.flow_collection_enabled == False:
        print 'INFO: Enabling VSS Flow Collection'
        sysconfig.flow_collection_enabled = True
        #sysconfig.stats_tsdb_server_address = "127.0.0.1:4242"
        sysconfig.save()
    else:
        print 'INFO: VSS Flow Collection is already enabled'


###########################################
# Creating Enterprise                     #
###########################################
def func_create_enterprise(csprootSession,enterpriseName,enterpriseLocalAS,infrastructure_org_profile):
    # Creating an enterprise
    my_enterprise = csprootSession.enterprises.get_first(filter="name == '%s'" % enterpriseName)
    if not my_enterprise:
        print 'INFO: Creating Enterprise', enterpriseName 
        my_enterprise = vspk.NUEnterprise(name=enterpriseName, local_as=enterpriseLocalAS, enterprise_profile_id=infrastructure_org_profile.id)
        csprootSession.create_child(my_enterprise)
    else:
        print 'INFO: Enterprise already created', enterpriseName
    
    return my_enterprise


###########################################
#  Create and Assign User to Enterprise 
#  admin group   
###########################################
def func_create_ent_users(csprootSession,userEntName,userEmail,EnterpriseName):
    cspenterprise = csprootSession.enterprises.get_first(filter="name == '%s'" % EnterpriseName)
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if userEntName not in lst_users:
        print 'INFO: Creating new Enterprise user', userEntName
        my_user = vspk.NUUser(first_name=userEntName, last_name=userEntName, 
                              user_name=userEntName, password=userEntName, email=userEntName+userEmail)
        cspenterprise.create_child(my_user)
    else:
        print 'INFO: New user', userEntName, 'is already created'
        my_user = cspenterprise.users.get_first(filter="userName=='%s'" % userEntName) 
    
    #when you assign a user to a group, it will remove the old users from the group
    # a workaround is get the append function before the assign function
    entadmingroup = cspenterprise.groups.get_first(filter="name=='Administrators'")
    admin_users = entadmingroup.users.get()
    lst_adminusersnames = [usradmin.user_name for usradmin in admin_users]
    if userEntName not in lst_adminusersnames:
        print 'INFO: Assign new user', userEntName, 'to group Admin'
        admin_users.append(my_user)
        entadmingroup.assign(admin_users, vspk.NUUser)
    else:
        print 'INFO: New user', userEntName, 'is already assigned to group root'


###########################################
# Creating domain templates               #
###########################################
def func_create_l3domain_template(new_enterprise,domainTemplateName,branchordc):    
    if branchordc=='branch':
        dpistatus='ENABLED'
        encryptionstatus='ENABLED'
    else:
        dpistatus='DISABLED'
        encryptionstatus='DISABLED'

    l3domtemp = new_enterprise.domain_templates.get_first(filter="name == '%s'" % domainTemplateName)
    if not l3domtemp: 
        print 'INFO: Creating Domain Template with DPI and Encryption', dpistatus
        # Create L3 domain Template
        l3domtemp = vspk.NUDomainTemplate(name=domainTemplateName,dpi=dpistatus,encryption=encryptionstatus)
        new_enterprise.create_child(l3domtemp)       
    else:
        print 'INFO: Domain Template is already created', domainTemplateName 

    return l3domtemp


###########################################
# Creating l3 domain with ACL rules       #
###########################################
def func_create_l3domain(domaintemplate,domainName,new_enterprise,domdescription,natflag,domencryption,domainDNS):    
    domains = new_enterprise.domains.get()
    lst_domains = [dom.name for dom in domains]
    if domainName not in lst_domains: 
        print 'INFO: Creating Domain', domainName
        # Create the domain on Enterprise.  
        new_domain = vspk.NUDomain(name=domainName,template_id=domaintemplate.id,
                                   description=domdescription,encryption=domencryption,
                                   underlay_enabled=natflag,pat_enabled=natflag)
        new_enterprise.create_child(new_domain)
        domdns = vspk.NUDHCPOption
        # Create a ntp option for the domain 
        #dhcp_option = vspk.NUDHCPOption(actual_type=4, actual_values=['130.20.30.1', '12.1.1.1'])
        # Create a DNS option for the domain 
        dhcp_option = vspk.NUDHCPOption(actual_type=6, actual_values=[domainDNS])
        new_domain.create_child(dhcp_option)   
        print 'INFO: Creating Allow ALL ACL rules in the Domain '
        # Define Allow All ingress and egress ACLs
        ingress_acl = vspk.NUIngressACLTemplate(name="Allow All",active=True,allow_address_spoof=True,
                                 policy_state="LIVE",default_allow_ip=True,default_allow_non_ip=True)
        new_domain.create_child(ingress_acl)
        egress_acl = vspk.NUEgressACLTemplate(name="Allow All",active=True,policy_state="LIVE",
                                              default_allow_ip=True,default_allow_non_ip=True)
        new_domain.create_child(egress_acl)

     
    else:
        print 'INFO: Domain is already created', domainName 
        for temp in domains:
            if temp.name == domainName:
    	        new_domain = temp 
    	        
    return new_domain


###########################################
# Creating zones                          #
###########################################
def func_create_zone(csprootSession,domain,zoneName,ZoneDecription):
    newzone = domain.zones.get_first(filter="name == '%s'" % zoneName)
    if not newzone:
        print 'INFO: Creating A Zone', zoneName
        newzone = vspk.NUZone(name=zoneName,description=ZoneDecription)
        domain.create_child(newzone)
    else:
        print 'INFO: Zone', zoneName, 'is already created'
    	        
    return newzone

###########################################
# Creating subnets                        #
###########################################
def func_create_subnet(csprootSession,zone,subnetName,zoneDescription,SubnetIpAddr,SubnetPrefix,dhcpminRange,dhcpmaxRange):
    new_subnet = zone.subnets.get_first(filter="name == '%s'" % subnetName)
    if not new_subnet:
        print 'INFO: Creating A Subnet', subnetName
        new_subnet=vspk.NUSubnet(name=subnetName,description=zoneDescription,address=SubnetIpAddr,netmask=SubnetPrefix)
        zone.create_child(new_subnet)

        # Define DHCP pools type BRIDGE in these subnets
        address_range_0=vspk.NUAddressRange(DHCP_pool_type="BRIDGE",min_address=dhcpminRange,max_address=dhcpmaxRange)
        new_subnet.create_child(address_range_0)
    else:
        print 'INFO: Subnet', subnetName, 'is already created'
    	        
    return new_subnet 


###########################################
# Creating NSG instance                   #
###########################################
def func_create_nsg(new_enterprise,nsgTemplate,NSGName):
    new_nsg = new_enterprise.ns_gateways.get_first(filter="name == '%s'" % NSGName)
    if not new_nsg:
        print 'INFO: Creating A New NSG instance', NSGName
        new_nsg=vspk.NUNSGateway(name=NSGName,template_id=nsgTemplate.id)
        new_enterprise.create_child(new_nsg)
        #new_enterprise.instantiate_child(new_nsg,nsgTemplate)
    else:
        print 'INFO: NSG instance', NSGName, 'is already created'


###########################################
# Start the script                        #
###########################################
def main():

    ############################################# 
    # create a new session
    ############################################# 
    session = vspk.NUVSDSession(username=username, password=password, 
        enterprise=enterprise, api_url=api_url)
    # start the session.
    try:
        session.start()
    except:
        print ('ERROR: Failed to start the session')
    
    csprootSession = session.user

    ###########################################
    #  Apply License
    ###########################################
    try:
        new_license = vspk.NULicense(license=myLicense)
        csprootSession.create_child(new_license)
        print 'INFO: Install License'
    except:
        print 'ERROR: License is rejected'

    ###########################################
    #  Create and Assign User to root group   #
    ###########################################
    func_create_users(session,userName1,userEmail)
    func_create_users(session,userName2,userEmail)

    ############################################# 
    # create VNS infrastructure - NSG profile
    ############################################# 
    infrastructure_gw_profile = func_create_infr_gw_profiles(csprootSession)

    ############################################# 
    # create two  VSC profile(s)
    ############################################# 
    infrastructure_vsc_profile1 = func_create_infr_vsc_profiles(csprootSession,infrVsc1Name,VSC1_IP)
    infrastructure_vsc_profile2 = func_create_infr_vsc_profiles(csprootSession,infrVsc2Name,VSC2_IP)

    ############################################# 
    # create VNS infrastructure - Access profile
    ############################################# 
    infra_access_profile = func_create_infr_access_profiles(csprootSession,infrAccessName,
        infrAccessUserName,infrAccessPassword)

    ######################################################
    # create 3 NSG templates (1WAN_1LAN, 2WAN_2LAN, 2WAN_4LAN)
    ######################################################
    nsgtemplate_1w_1l = func_create_nsg_1w_1l_template(csprootSession,nsgTemplate1Name,infrastructure_gw_profile,
        infra_access_profile,infrastructure_vsc_profile1,infrastructure_vsc_profile2)

    nsgtemplate_2w_2l = func_create_nsg_2w_2l_template(csprootSession,nsgTemplate2Name,infrastructure_gw_profile,
        infra_access_profile,infrastructure_vsc_profile1,infrastructure_vsc_profile2)

    nsgtemplate_2w_4l = func_create_nsg_2w_4l_template(csprootSession,nsgTemplate3Name,infrastructure_gw_profile,
        infra_access_profile,infrastructure_vsc_profile1,infrastructure_vsc_profile2)

    ###########################################
    # Creating Advanced Organization Profile  #
    ###########################################
    infrastructure_org_profile = func_create_infr_org_profiles(csprootSession,infrOrganizationProfileName)

    ###########################################
    # Enable the VSS Flow collection flag in the system configuration
    ###########################################
    func_enable_vss_flow_collection(session)

    ############################################# 
    # create a new Enterprise
    ############################################# 
    new_enterprise = func_create_enterprise(csprootSession,enterpriseName,
                                            enterpriseLocalAS,infrastructure_org_profile)

    ############################################# 
    # create a new Enterprise User admin and assign him to group admin
    ############################################# 
    func_create_ent_users(csprootSession,userEntName1,userEmail,enterpriseName)
    
    ############################################# 
    # create a new Domain template for branch (encr) and DC (non-encry)
    ############################################# 
    # create a new Domain template; one for branch and one for dc
    new_br_domain_template = func_create_l3domain_template(new_enterprise,brdomainTemplate,branchordc='branch')
    new_dc_domain_template = func_create_l3domain_template(new_enterprise,dcdomainTemplate,branchordc='dc')
    
    ############################################# 
    # create a new Branch Domain, Zones, Subnets
    ############################################# 
    # create a new branch encrypted Domain
    domdescription='Encrypted domain'
    natflag='ENABLED'
    domencryption='ENABLED'
    new_br_domain = func_create_l3domain(new_br_domain_template,brdomainName,new_enterprise,
                                        domdescription,natflag,domencryption,domainDNS)
    
    # create a new branch Zones
    new_zone1 = func_create_zone(csprootSession,new_br_domain,zone1Name,zone1Description)
    new_zone2 = func_create_zone(csprootSession,new_br_domain,zone2Name,zone2Description)
    new_zone3 = func_create_zone(csprootSession,new_br_domain,zone3Name,zone3Description)

    # create a new subnets
    subnet1_zone1 = func_create_subnet(csprootSession,new_zone1,subnet1Name,zone1Description,subnet1IpAddr,
                                           subnet1Prefix,subnet1DhcpMinRange,subnet1DhcpMaxRange)
    subnet2_zone1 = func_create_subnet(csprootSession,new_zone1,subnet2Name,zone1Description,subnet2IpAddr,
                                           subnet2Prefix,subnet2DhcpMinRange,subnet2DhcpMaxRange)
    subnet1_zone2 = func_create_subnet(csprootSession,new_zone2,subnet3Name,zone2Description,subnet3IpAddr,
                                           subnet3Prefix,subnet3DhcpMinRange,subnet3DhcpMaxRange)
    subnet1_zone3 = func_create_subnet(csprootSession,new_zone3,subnet4Name,zone3Description,subnet4IpAddr,
                                           subnet4Prefix,subnet4DhcpMinRange,subnet4DhcpMaxRange)
    subnet2_zone3 = func_create_subnet(csprootSession,new_zone3,subnet5Name,zone3Description,subnet5IpAddr,
                                           subnet5Prefix,subnet5DhcpMinRange,subnet5DhcpMaxRange)

    ############################################# 
    # create a new "DC" Domain, Zones, Subnets
    ############################################# 
    # create a new DC non-encrypted Domain
    domdescription='No Encryption domain'
    natflag='ENABLED'
    domencryption='DISABLED'
    new_dc_domain = func_create_l3domain(new_dc_domain_template,dcdomainName,new_enterprise,
                                        domdescription,natflag,domencryption,domainDNS)
    # create a new branch Zones
    new_dc_zone1 = func_create_zone(csprootSession,new_dc_domain,dczone1Name,dczone1Description)
    # create a new subnets
    dc_subnet1_zone1 = func_create_subnet(csprootSession,new_dc_zone1,dcsubnet1Name,dczone1Description,dcsubnet1IpAddr,
                                           dcsubnet1Prefix,dcsubnet1DhcpMinRange,dcsubnet1DhcpMaxRange)
    dc_subnet2_zone1 = func_create_subnet(csprootSession,new_dc_zone1,dcsubnet2Name,dczone1Description,dcsubnet2IpAddr,
                                           dcsubnet2Prefix,dcsubnet2DhcpMinRange,dcsubnet2DhcpMaxRange)
    dc_subnet3_zone1 = func_create_subnet(csprootSession,new_dc_zone1,dcsubnet3Name,dczone1Description,dcsubnet3IpAddr,
                                           dcsubnet3Prefix,dcsubnet3DhcpMinRange,dcsubnet3DhcpMaxRange)
    dc_subnet4_zone1 = func_create_subnet(csprootSession,new_dc_zone1,dcsubnet4Name,dczone1Description,dcsubnet4IpAddr,
                                           dcsubnet4Prefix,dcsubnet4DhcpMinRange,dcsubnet4DhcpMaxRange)

    ############################################# 
    # create 3 New NSGs Instances; one from each template
    ############################################# 
    func_create_nsg(new_enterprise,nsgtemplate_1w_1l,NSGName1)
    func_create_nsg(new_enterprise,nsgtemplate_2w_2l,NSGName2)
    func_create_nsg(new_enterprise,nsgtemplate_2w_4l,NSGName3)
    
 
    #sys.exit()
    
    #new_enterprise = vspk.NUEnterprise(name=enterpriseName)
    #new_enterprise.description = "cool"
    #csprootSession.create_child(new_enterprise)
    #new_enterprise.name = "mycopr"
    #new_enterprise.save()
    #new_enterprise.delete()    
    
if __name__ == "__main__":
   main()
