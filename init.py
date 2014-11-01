""" responsible for managing the initialization
	of other plugins on the client
"""
class init(Plugin):
	name = "init"
	
	parameters = []


	''' ocean-client sends a list of it's locally
		installed plugins to the server-side ocean-bot
	'''
	def sendListOfLocalPlugins(self):
