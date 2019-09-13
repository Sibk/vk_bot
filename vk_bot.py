#!/usr/bin/python3

from routing import Route
import vk_api, re, threading
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload

class Session_bot:

	__MY_TOKEN = ''
	__GROUP_TOKEN = ''
	__FILE_TOKEN = '/home/malina/scripts/bot/tokens.txt'
	GROUP_VK_SESSION = ''
	MY_VK_SESSION = ''
	VERSION = '5.101'
	

	def __get_tokens(self):
		file = open(self.__FILE_TOKEN)
		for line in file:
			if(re.search(r'my_token', line)): self.__MY_TOKEN = re.findall(r'\s(\w+)', line)[0]
			if(re.search(r'group_token', line)): self.__GROUP_TOKEN = re.findall(r'\s(\w+)', line)[0]
		file.close()

	def __get_api(self):
		self.GROUP_VK_SESSION = vk_api.VkApi(token = self.__GROUP_TOKEN)
		self.MY_VK_SESSION = vk_api.VkApi(token = self.__MY_TOKEN)
		longpoll = VkLongPoll(self.GROUP_VK_SESSION)
		upload = VkUpload(self.GROUP_VK_SESSION)

		api = { 'group' : self.GROUP_VK_SESSION.get_api(),
				'my': self.MY_VK_SESSION.get_api(),
				'longpoll' : longpoll,
				'upload' : upload
			}
		return api

	def start_session(self):
		self.__get_tokens()
		api = self.__get_api()
		return api

	def test(self):
		self.__get_tokens()


class Front_controller:

	def start_bot(self):
		#В этом классе запускаются все процедуры запуска сессии
		session_bot = Session_bot()
		route = Route() #Маршрутизация запросов
		api = session_bot.start_session()

		#Запуск LONG POLL сообщества
		for event in api['longpoll'].listen(): #Прослушка входящих сообщений сообщества
			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
				t = threading.Thread(target = route.routing, args = (event, api))
				t.daemon = True
				t.start()
				#route.routing(event, api) #передаем событие на маршрутизацию
				print('Кол-во потоков: {}'.format(threading.activeCount()))

if __name__ == '__main__':
	front = Front_controller()
	front.start_bot()
