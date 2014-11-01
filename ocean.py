import threading
from time import sleep

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol


class Plugin(object):
    """ A generic interface for client-server plugins
    """
    name = "plugin-default"
    parameters = []
    version = 0
    cache-updated = 0

    # Initialization
    def generateInitParams(self):
        """ (client side) generates a list of parameters 
            that report the state of the client 
        """
        json.dumps({"version": parameters[version], "cache-updated": parameters[cache-updated]})
        

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




class OceanClient(irc.IRCClient):

    nickname = ''
    password = ''

    plugins = {}
    listeners = {}

    def __init__(self, factory):
        self.factory = factory
        self.plugins = self.factory.plugins
        self.nickname = self.factory.nickname

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "connection made"
 
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "connection lost" 

    def generateInitParams(self):
        initParams = {}
        for key in plugins.keys:
            json[key] = plugins[key].generateInitParams()
        return "\"init\": "+initParams


class OceanClientFactory(protocol.ClientFactory):

    protocol = OceanClient

    def __init__(self, nick):
        self.channel = "#general";
        self.plugins = loadPlugins()
        self.nickname = nick

    def buildProtocol(self, addr):
        return OceanClient(self)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        print("reconnecting...")
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print("connection failed: %s"%(reason,))
        reactor.stop()

def loadPlugins():
    return []

class OceanBot(object):
    
    def __init__():
        pass