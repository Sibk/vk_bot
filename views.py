#!/usr/bin/python3
from vk_api.utils import get_random_id
from google_images_download import google_images_download
import requests, random

class Views:
	BUTTON1 = '{"one_time" : false, "buttons" : [ \
				[{"action":{"type" : "text", "label" : "button"}, "color": "negative"}] \
			]}'

	def welcome(self, api, user_id):
		attachments = []
		image_path = '/home/malina/images/welcome.png'
		photo = api['upload'].photo_messages(photos = image_path)[0]
		attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
		api['group'].messages.send(user_id = user_id, 
				message = 'Здарова мешок с костями', 
				attachment=','.join(attachments), 	
				keyboard = self.BUTTON1, 
				random_id=get_random_id()
				)
		print('welcome')

	def brobot_dialog(self, request, api, user_id):
		text = '{}'.format(request['result']['fulfillment']['speech'])
		api['group'].messages.send(user_id = user_id, message = text, random_id=get_random_id()) 

	def show_bobs(self, request, api, user_id):
		attachments = []
		session = requests.Session()
		text = '{}'.format(request['result']['fulfillment']['speech'])
		response = google_images_download.googleimagesdownload()
		argument = {'keywords' : 'красивые сиськи', 
		'limit' : 100, 
		'print_urls': True, 
		'no_download' : True,
		'silent_mode' : True, 
		"size": "large", 
		'format' : 'jpg',
		'type' : 'photo',
		'time' : 'past-7-days'
		}
		absolute_image_paths = response.download(argument)
		i = random.randint(0, 99)
		image = session.get(absolute_image_paths[0]['красивые сиськи'][i], stream=True)
		photo = api['upload'].photo_messages(photos=image.raw)[0]
		attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
		api['group'].messages.send(user_id = user_id, 
				message = text, 
				attachment=','.join(attachments), 	
				keyboard = self.BUTTON1, 
				random_id=get_random_id()
				)