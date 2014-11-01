import irc
import simplejson

class Plugin(Object):
	""" A generic interface for client-server plugins
	"""
	name = "plugin-default"
	parameters = []


	# Initialization

	def generateInitParams(self):
		""" (client side) generates a list of parameters 
			that report the state of the client 
		"""
		pass

	def parseInitParams(self, json):
		""" (server side) parses down the list of init
			params from the client and shits out a list
			of the neccisary data to update the state of
			the client to the state of the server
		"""
		pass

	def initializeClient(self, json):
		""" (client side) updates the client from 
			parseInitParams to be in sync with the server
		"""
		pass


	# Updating (we don't care about these for now)
	# also it's not finished right now

	def updateServer(self, json):
		""" update some parameter in the ser
		"""

	def updateClient(self, json):
		""" (client side) update the client from a change
			in the server.
		"""
		pass

class OceanClient(Object):

	ircClient = None
	connection = None

	plugins = {}
	listeners = {}

	def __init__(self):
		self.ircClient = irc.client.IRC()

	def addPlugin(self, plugin):
		plugins[plugin.name] = plugin


	def registerListener(self, pluginName, name):
		if string not in listeners.keys:
			listeners[string] = []

		listeners[string].append(self.plugins[pluginName])

	def connectAndInit(self, server, port, nick):
		self.connection = self.ircClient.server()
		outgoingMessage = self.generateInitParams();
		self.connection.connect(server, port, nick)

	def generateInitParams(self):
		initParams = {}
		for key in plugins.keys:
			json[key] = plugins[key].generateInitParams()
		return initParams

class OceanBot(Object):
	
	def __init__():
		pass