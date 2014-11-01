import ocean.property
from urlparse import urlparse
from flask import request
import urllib2
import simplejson

""" handles the tab completion engine 
	and dialog (client side only)
"""
class tab-completion(Plugin):
	name = "tab-completion"
	#register to listen for just `keystrock` event hook
	parameters = []
	listofCommands = ['invite', 'join',
						'kick', 'leave', 'dm', 'shrug', 'topic', 'who']

	""" return all commands in a json file
	"""
	def getCommands(self, currentText):
		return simplejson.dumps({"listofCommands": listofCommands})

""" command functions start here
"""

	def invite(self, invitee):
		#check if the invitee is already in the channel or not
		
		#if invitee isnt in channel list, send an invite to the 
		#invitee



	def join(self, newChannel):
		

	def kick(self, user):

	def leave(self):

	def dm(self, user, message):


	def shrug(self, message):


	def topic(self, topic):

	def who(self):




