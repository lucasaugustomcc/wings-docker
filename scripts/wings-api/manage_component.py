import os
import json
import argparse
import wings.component

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server", 
	default="http://localhost:8080/wings-portal")
parser.add_argument("-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password", help="Portal admin password", default="4dm1n!23")
parser.add_argument("-dom", "--domain", help="Portal domain")
parser.add_argument("-n", "--new", help="Create operation", action="store_true")
parser.add_argument("-c", "--component_id", help="Component id")
parser.add_argument("-ct", "--component_type", help="Component type")
parser.add_argument("-save", "--save_component", help="Save or update component info (filename with json data)")
parser.add_argument("-init", "--initialize_code", help="Initialize component code")
parser.add_argument("-lang", "--language_code", help="Programming Language", default="Generic")
parser.add_argument("-code", "--save_code", help="Save component code")
parser.add_argument("-path", "--script_path", help="Define script path location", default="run")
parser.add_argument("-pt", "--parent_type", help="Component type's Parent (for creating new component type)")
parser.add_argument("-pc", "--parent_component_id", help="Component's Parent (for creating new component)")
parser.add_argument("-g", "--get", help="Get information (use either with component_id, component_type or none)", action="store_true")
args = parser.parse_args()

# Create manage user api
component = wings.ManageComponent(args.server, args.userid, args.domain)

# Login with password
if component.login(args.password): 
	if args.new:
		if args.component_id:
			component.add_component_for_type(args.component_id, args.parent_type, args.parent_component_id)
		elif args.component_type:
			component.new_component_type(args.component_type, args.parent_type)
	elif args.save_component:
		with open(args.save_component) as dfile:    
			jsonobj = json.load(dfile)
			component.save_component(jsonobj)
	elif args.initialize_code and args.component_id:
			component.inicialize_component_code(args.component_id, args.language_code)
	elif args.save_code and args.component_id:
			with open(args.save_code) as dfile:
				component.save_component_code(args.component_id, dfile.read(), args.script_path)
	elif args.get:
		if args.component_id:
			print(component.get_component_description(args.component_id))
		elif args.component_type:
			print(component.get_component_type_description(args.component_type))
	# Logout
	component.logout()
