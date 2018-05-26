import json
import requests
from Function import Function
import wings.component
 
server = 'http://localhost:8080/wings-portal'
userid = 'lucas'
password = 'lucas'
domain = 'DMDomain'

ontosoft_server = "http://localhost:8080/ontosoft-server"
function = "software/Software-QUrZXB1D5rlR/version/SoftwareVersion-0l00sGxRXUe1/function/Function-GAuvALBVGoBh"
ontns = "http://ontosoft.org/software#"

#resp = requests.get( server + "/" + function )
#data = resp.json()['value']
with open("/home/lucas/Desktop/integration/function.json") as file:
	 data = json.load(file)['value']

managedata = wings.ManageData(server, userid, domain)
managedata.login(password)

func = Function(ontns)
func.extractData(data, managedata)

managedata.logout()

print "FunctionName: " + func.name
print "Functionality: " + func.functionality
print "Inputs: " + str(func.inputs)
print "Outputs: " + str(func.outputs)

code = func.getCode()

jsonobj = func.getJSON()

# Create manage component api
component = wings.ManageComponent(server, userid, domain, "/home/lucas/.wings")

# Login with password
component.login(password)
component.add_component_type(func.functionality)
component.add_component_for_type(func.name, func.functionality)
component.save_component(func.name, jsonobj)
component.initialize_component_code(func.name)
component.save_component_code(func.name, code)

# Logout
component.logout()