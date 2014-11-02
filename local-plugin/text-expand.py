import ocean.property
from urlparse import urlparse
from flask import request
import urllib2

""" expands images, gifs, webpages and 
	youtube videos linked in chat (client side only)
"""
class link-expand(Plugin):
	name = "list-expand"
	#register to listen for just `message-send` event hook
	parameters = []
	version = 1


	''' checks if a link is in the message
	'''
	def urlChecker(self, message):
		#list of all strings that could be links
		possible_urls = re.findall(r'http://\S+', text)
		
		#we only want the first one, also nicely checks if we 
		#have one at all or not
		if len(possible_urls) >= 1:
			determineLinkType(text)

	""" determines the link type of the first url
	"""
	def determineLinkType(self, message):
		#parse it to see if its a youtube video because thats easy
		#example, http://youtu.be/gNZ7FA6eIzw
		possible_youtube_url = re.findall(r'http://youtu.be\S+', text)
		if len(possible_youtube_url) >= 1:
			expandVideo(possible_youtube_url[0])

		#also we can parse to see if its a nicely put url for an image for instance
		#example: http://static.fjcdn.com/pictures/Horsedick_dfbb39_424378.jpg
		possible_pic_url = re.findall(r'\S+.jpg', text)
		if len(possible_pic_url) >= 1:
			expandImage(possible_pic_url[0])
		else: #nothing else has worked, lets check through other means

			#submit a GET on the url
			r = requests.get(possible_urls[0])
			#access the headers to get the content type
			urlHeaders = r.headers['content-type']
			#regex to get the specific content type
			contentType = re.findall(r'\S;', urlHeaders)

			#check if its an image
			if contentType == 'image/jpeg':
				expandImage(possible_urls[0])
			#check if its a gif
			if contentType == 'image/gif':
				expandGIF(possible_urls[0])
			#check if its a regular website
			if contentType == 'text/html':
				expandWebpage(possible_urls[0])


	
	""" will send back the image link back to 
		the message feed controller
	"""
	def expandImage(self, link):


	""" will send back the GIF link back to 
		the message feed controller
	"""
	def expandGIF(self, link):



	""" will send back the Webpage title
		and description back to 
		the message feed controller
	"""
	def expandWebpage(self, link):


	""" will send back youtube data to
		message feed controller
	"""
	def expandVideo(self, link):


#
#parameters[version] = 1.0
#parameters[cache-updated] = datetime.datetime.now()		



	
