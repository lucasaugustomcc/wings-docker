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

	def get_componenttype_description(self, ctype):
		ctype = self.get_type_id(ctype)
		paramdata = { 'cid': ctype }
		resp = self.session.get( self.get_request_url() + 'components/type/getComponentJSON', params = paramdata )
		return resp.json()

	def get_component_description(self, cid):
		cid = self.get_component_id(cid)
		paramdata = { 'cid': cid }
		resp = self.session.get( self.get_request_url() + 'components/getComponentJSON', params = paramdata )
		return resp.json()
