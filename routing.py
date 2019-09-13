#!/usr/bin/python3
from views import Views
import apiai, json

class Route:
	views = Views()
	

	route_table = [
		{'route' : 'Начать', 'func' : views.welcome},
		{'route': 'bobs', 'func' : views.show_bobs},
		{'route': 'brobot_dialog', 'func' : views.brobot_dialog}, #пустая болтовня, роута нет
	]

	def routing(self, event, api):
		request = self.__brobot_ai(event)
		for route in self.route_table:
			if(route['route'] == request['result']['parameters']['custom']): #проверка роута через ai
				route['func'](request, api, event.user_id) 
				break
			elif(route['route'] == event.text): #проверка прямого роута
				route['func'](api, event.user_id)
				break


	def __brobot_ai(self, event):
		request = apiai.ApiAI('9e0665b144cd4e5994b77bcdf666d15c').text_request()
		request.lang = 'ru'
		request.session_id = 'brobot'
		request.query = event.text #добавляем пользовтельский запрос
		req = request.getresponse().read().decode('utf-8') #отсылаем на dialogflow, получаем текстом JSON
		print(req)
		result = json.loads(req) #переводим текстовую переменную в dict
		if(not result['result']['parameters']): result['result']['parameters']['custom'] = 'brobot_dialog'
		return result 
