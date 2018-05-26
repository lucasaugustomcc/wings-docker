import os
import re
import json
from .userop import UserOperation

class ManageComponent(UserOperation):

	def __init__(self, server, userid, domain, location=""):
		super(ManageComponent, self).__init__(server, userid, domain)
		self.libns = self.get_export_url() + "components/library.owl#"
		self.dcdom = self.get_export_url() + "data/ontology.owl#"
		self.xsdns = "http://www.w3.org/2001/XMLSchema#"
		self.topcls = "http://www.wings-workflows.org/ontology/component.owl#Component"
		self.location = location + "/storage/users/" + userid + "/" + domain + "/code/library/"

	def get_type_id(self, typeid):
		if typeid == None:
			return self.topcls
		elif not re.match( r"(http:|https:)//", typeid ):
			return self.libns + typeid
		else:
			return typeid

	def get_component_id(self, cid=None):
		if cid == None:
			return "" 
		elif not re.match( r"(http:|https:)//", cid ):
			return self.libns + cid
		else:
			return cid

	def add_component_type(self, cid, parent_type=None, parent_cid=None):
		parent_type = self.get_type_id(parent_type)
		parent_cid = self.get_type_id(parent_cid)
		cid = self.get_type_id(cid)
		postdata = { 'parent_type': parent_type , 'parent_cid': parent_cid, 'cid': cid }
		resp = self.session.post( self.get_request_url() + 'components/type/addComponent', postdata )
		assert resp.content == "OK"

	def add_component_for_type(self, cid, parent_cid, parent_type=None):
		parent_cid = self.get_component_id(parent_cid)
		parent_type = parent_cid + "Class"
		cid = self.get_component_id(cid)
		postdata = { 'cid': cid, 'load_concrete': True, 'parent_cid': parent_cid, 'parent_type': parent_type }
		resp = self.session.post( self.get_request_url() + 'components/addComponent', postdata )
		assert resp.content == "OK"

	def get_component_type_description(self, ctype):
		ctype = self.get_type_id(ctype)
		paramdata = { 'cid': ctype }
		resp = self.session.get( self.get_request_url() + 'components/type/getComponentJSON', params = paramdata )
		return resp.json()

	def get_component_description(self, cid):
		cid = self.get_component_id(cid)
		paramdata = { 'cid': cid }
		resp = self.session.get( self.get_request_url() + 'components/getComponentJSON', params = paramdata )
		return resp.json()

	def initialize_component_code(self, cid, language="Generic"):
		cid = self.get_component_id(cid)
		postdata = { 'cid': cid, 'language': language }
		self.session.post( self.get_request_url() + 'components/fb/initialize', postdata )

	def save_component_code(self, cid, code, path="run"):
		cid = self.get_component_id(cid)
		postdata = { 'cid': cid, 'path': path, 'filedata': code }
		resp = self.session.post( self.get_request_url() + 'components/fb/save', postdata )

	def save_component(self, cid, metadata):
		jsonobj = self._modify_component_json(cid, metadata)
		jsonobj["type"] = 2
		print json.dumps(jsonobj)
		postdata = { 'load_concrete': True, 'component_json': json.dumps(jsonobj) }
		resp = self.session.post( self.get_request_url() + 'components/saveComponentJSON', postdata )
		assert resp.content == "OK"

	def _modify_component_json(self, cid, jsonobj):
		for input in jsonobj["inputs"]:
			input["type"] = input["type"].replace("xsd:", self.xsdns)
			input["type"] = input["type"].replace("dcdom:", self.dcdom)
			input["id"] = self.get_component_id(cid) + "_" + input["role"]
		for output in jsonobj["outputs"]:
			output["type"] = output["type"].replace("xsd:", self.xsdns)
			output["type"] = output["type"].replace("dcdom:", self.dcdom)
			output["id"] = cid + "_" + output["role"]
		jsonobj["id"] = self.get_component_id(cid)
		jsonobj["location"] = self.location + cid
		return jsonobj
