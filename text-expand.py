import ocean.property
from urlparse import urlparse

class link-expand(Plugin):
	""" expands images, webms and 
		youtube videos linked in chat (client side only)
	"""
	name = "plugin-default"
	parameters = []

	''' if a link is in the message, determine the
		link type and call the appropriate function
	'''
	def determineLinkType(self, message):
		#list of all strings that could be links
		possible_urls = re.findall(r'https?://\S+', text)
		
		#submit a GET on the url

		#scan the meta data

		#we only want the first one, also nicely checks if we 
		#have one at all or not
		if len(possible_urls) >= 1:
			url = urlparse(possible_urls[0])


	def expandImage(self, link):




	def expandWebpage(self, link):


	def expandVideo(self, link):


#json.dumps({"version": parameters[version], "cache-updated": parameters[cache-updated]})
#parameters[version] = 1.0
#parameters[cache-updated] = datetime.datetime.now()		



	
