class Function:
	def __init__(self, ontns):
		self.name = ""
		self.inputs = []
		self.params = []
		self.outputs = []
		self.algorithm = ""
		self.functionality = "" 
		self.invocation_code = ""
		self.ontns = ontns

	def getCode(self):
		code = """#!/bin/bash

checkExitCode() {
if [ $? -ne 0 ]; then
    echo "Error"
    exit 1;
fi
}

BASEDIR=`dirname $0`

. $BASEDIR/io.sh """ + str(sum([1 for input in self.inputs if input['isParam'] == False])) + " " + str(sum([1 for input in self.inputs if input['isParam'] == True])) + " " + str(sum([1 for i in self.outputs])) + """ "$@"

""" + self.invocation_code + " " + (" ").join(["$INPUTS"+str(i) for i,input in enumerate(self.inputs,1) if input['isParam'] == False]) + " " + (" ").join(["$PARAMS"+str(i+1) for i,input in enumerate(self.inputs) if input['isParam'] == True]) + " " + (" ").join(["$OUTPUTS"+str(i+1) for i,output in enumerate(self.outputs)]) + """

checkExitCode
"""
		return code

	def getJSON(self):
		jsonobj = {
			"inputs":self.inputs,
		   	"outputs":self.outputs,
		   	"rulesText":"",
		   	"requirement":{
		      	"softwareIds":[

		      	],
		      	"memoryGB":"0",
		      	"storageGB":"0",
		      	"needs64bit":False
		   	}
		}
		return jsonobj

	def extractData(self, data, managedata):
		for property in data.keys():
			if property == self.ontns + "hasFunctionName":
				self.name = data[property][0]['value']
			elif property == self.ontns + "hasFunctionality":
				self.functionality = data[property][0]['value'].replace(" ","")
			elif property == self.ontns + "hasInputFile":
				for input in data[property]:
					obj = {}
					for i,value in enumerate(input['value'],1):
						if value == self.ontns + "hasInputFileName":
							if input['value'][value][0]['value'] == "":
								obj = {}
								break
							obj['role'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasInputFileDataType":
							type = input['value'][value][0]['value']
							obj['type'] = 'dcdom:' + type
							managedata.new_data_type(type, None)
						elif value == self.ontns + "hasInputFileDataFormat":
							obj['format'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasInputFileArgument":
							obj['prefix'] = input['value'][value][0]['value'] if len(input['value'][value]) > 0 else "-i"+str(i)
						obj['dimensionality'] = 0
						obj['isParam'] = False
					if obj != {}:
						managedata.add_type_properties(obj['type'], { 'hasDataFormat': 'Domain', 'hasDataType': 'Domain' })
						if not 'prefix' in obj:
							obj['prefix'] = "-i" + str(len(self.params)+1)
						self.inputs.append(obj)
			elif property == self.ontns + "hasInputParameter":
				for input in data[property]:
					obj = {}
					for i,value in enumerate(input['value'],1):
						if value == self.ontns + "hasInputParameterName":
							if input['value'][value][0]['value'] == "":
								obj = {}
								break
							obj['role'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasInputParameterDataType":
							type = input['value'][value][0]['value']
							obj['type'] = 'xsd:' + type.lower()
						elif value == self.ontns + "hasInputParameterDefaultValue":
							obj['paramDefaultValue'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasInputParameterArgument":
							obj['prefix'] = input['value'][value][0]['value'] if len(input['value'][value]) > 0 else "-p"+str(i)
						obj['dimensionality'] = 0
						obj['isParam'] = True
					if obj != {}:
						if not 'prefix' in obj:
							obj['prefix'] = "-p" + str(len(self.params)+1)
						self.inputs.append(obj)
						self.params.append(obj)
			elif property == self.ontns + "hasOutput":
				for input in data[property]:
					obj = {}
					for i,value in enumerate(input['value'],1):
						if value == self.ontns + "hasOutputName":
							if input['value'][value][0]['value'] == "":
								obj = {}
								break
							obj['role'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasOutputDataFormat":
							obj['format'] = input['value'][value][0]['value']
						elif value == self.ontns + "hasOutputDataType":
							type = input['value'][value][0]['value']
							obj['type'] = 'dcdom:' + type
							managedata.new_data_type(type, None)
						elif value == self.ontns + "hasOutputArgument":
							obj['prefix'] = input['value'][value][0]['value'] if len(input['value'][value]) > 0 else "-o"+str(i)
						obj['dimensionality'] = 0
						obj['isParam'] = False
					if obj != {}:
						managedata.add_type_properties(obj['type'], { 'hasDataFormat': 'Domain', 'hasDataType': 'Domain' })
						if not 'prefix' in obj:
							obj['prefix'] = "-o" + str(len(self.outputs)+1)
						self.outputs.append(obj)
			elif property == self.ontns + "hasFunctionInvocation":
				self.invocation_code = data[property][0]["value"]

	def getRules(self):
		rule = """[ 
			checkDataTypeAndDataFormat: 
				print(Firing checkDataTypeAndDataFormat) 
				(?c rdf:type acdom:""" + self.name + """Class) 
				(?c ac:hasInput ?idv)
				(?idv ac:hasArgumentID '""" + self.inputs[0]['role'] + """')
				(?idv dcdom:hasDataFormat ?format)
				(?idv dcdom:hasDataType ?type)
				notEqual(""" + self.inputs[1]['format'] + """ ?format)
				notEqual(""" + self.inputs[0]['type'] + """ ?type) 
					-> (?c ac:isInvalid "true"^^xsd:boolean) 
				print(Template is invalid because ?idv has data type or format that """ + self.name + """ cannot consume BayesModels) 
		]"""
		return [rule]