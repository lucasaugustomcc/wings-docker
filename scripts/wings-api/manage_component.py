import os
import json
import argparse
import wings.data

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server", 
	default="http://localhost:8080/wings-portal")
parser.add_argument("-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password", help="Portal admin password", default="4dm1n!23")
parser.add_argument("-dom", "--domain", help="Portal domain")
parser.add_argument("-c", "--component_id", help="Component id")
parser.add_argument("-ct", "--component_type", help="Component type")
parser.add_argument("-g", "--get", help="Get information (use either with component_id, component_type or none)", action="store_true")
args = parser.parse_args()

# Create manage user api
component = wings.ManageComponent(args.server, args.userid, args.domain)

# Login with password
if component.login(args.password): 
	if args.get:
		if args.component_id:
			print(component.get_component_description(args.component_id))
		elif args.component_type:
			print(component.get_componenttype_description(args.component_type))
	# Logout
	component.logout()
