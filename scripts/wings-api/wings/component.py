import os
import re
import json
from .userop import UserOperation

class ManageComponent(UserOperation):

	def __init__(self, server, userid, domain):
		super(ManageComponent, self).__init__(server, userid, domain)
		self.cclib = self.get_export_url() + "components/library.owl#"

	def get_type_id(self, typeid):
		if not re.match( r"(http:|https:)//", typeid ):
			return self.cclib + typeid
		else:
			return typeid

	def get_component_id(self, cid):
		if not re.match( r"(http:|https:)//", cid ):
			return self.cclib + cid
		else:
			return cid

	def add_component_type(self, ctype, parent):
		parent = self.get_type_id(parent)
		ctype = self.get_type_id(ctype)
		postdata = { 'parent_type': parent , 'cid': ctype }
		self.session.post( self.get_request_url() + 'components/type/addComponent', postdata )

	def add_component_for_type(self, cid, parent_type, parent_cid):
		parent_cid = self.get_component_id(parent_cid)
		parent_type = self.get_type_id(parent_type)
		cid = self.get_component_id(cid)
		postdata = { 'parent_cid': parent_cid, 'parent_type': parent_type, 'cid': cid }
		self.session.post( self.get_request_url() + 'components/addComponent', postdata )

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
		resp = self.session.post( self.get_request_url() + 'components/fb/initialize', postdata )
		return resp.json()

	def save_component_code(self, cid, code, path="run"):
		cid = self.get_component_id(cid)
		postdata = { 'cid': cid, 'path': path, 'filedata': code }
		resp = self.session.post( self.get_request_url() + 'components/fb/save', postdata )

	def save_component(self, metadata):
		postdata = { 'component_json': json.dumps(metadata) }
		self.session.post( self.get_request_url() + 'components/saveComponentJSON', postdata )
