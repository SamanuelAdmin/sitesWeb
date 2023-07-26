import socket

import threading

import os

import random

import time

from colorama import init
init()
from colorama import Fore, Back, Style

from datetime import datetime

import re

import urllib




class Main:

	def __init__(self, ip, port=7000):
		self.send_message_form = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<!--meta http-equiv="Refresh" content="60" />-->
	<title>Forum | Dark Web</title>
</head>
<body style="background: rgb(0, 0, 0) ; color: rgb(183, 190, 187);">
<h1 style="font-size: 2.5em; text-align: left;">Dark Web</h1>

<a href="/forum.html">UPDATE</a>
<br>

<form action="/forum_send.html" method="get" style="text-align: center; float: right; padding: 1em; font-size: 2em;">
	<label for="name" value="Anonimous" autocomplete="on">Name: </label>
	<input type="text" id="name" name="user_name" maxlength="10" style="font-size: 1em;">
	<br>
	<br>
	<label for="msg">Message: </label>
	<textarea id="msg" name="user_message" maxlength="100" style="font-size: 1.2em;"></textarea>
	<br>
	<br>
	<button type="submit" style="font-size: 1em;">Send your message</button>
</form>
<br>
<br>
		'''

		self.notifboard_temps = ['''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Notifications | Dark Web</title>
</head>
<body style="background: rgb(0, 0, 0) ; color: rgb(183, 190, 187);">
	<h1 style="font-size: 2.5em; text-align: left;">Dark Web</h1>
	<p style="font-size: 4em; text-align: center;">Notifications:</p>
	<hr>
	<br>

	<form action="/notifboard" method="get" style="margin: 0 auto; width: 400px; padding: 1em; border: 1px solid #CCC; border-radius: 1em;">
		<div>
			<label style="display: inline-block; width: 90px; text-align: right;" for="price" maxlength="6">Price: </label>
			<input type="text" id="price" name="user_name" />
		</div>
		<div>
			<label style="display: inline-block; width: 90px; text-align: right;" for="title" maxlength="30">Title: </label>
			<input id="mail" name="title" />
		</div>
		<div>
			<label style="display: inline-block; width: 90px; text-align: right;" for="description" maxlength="150">Description: </label>
			<textarea id="msg" name="description" style="height: 6em;"></textarea>
		</div>
		<div>
			<label style="display: inline-block; width: 90px; text-align: right;" for="link" maxlength="40">Link: </label>
			<textarea id="msg" name="link"></textarea>
		</div>
		<br>
		<button type="submit" style="font-size: 1em;">SEND</button>
	</form>

	''', '''</body>
</html>''']


		self.__IP__ = (ip, int(port))

		self.stocks_ports = [3543, 9874, 873, 354, 12353]

		self.MAIN_SERVER = None

		self.main_path = os.getcwd()

		self.templates = {}

		for woo in os.walk(self.main_path + '\\templates'):
			for file in woo[2]:
				self.templates[file] = open(self.main_path + f'\\templates\\{file}', 'rb')

		self.__print('Configs has been setted.', status = None)


	def __create_responce(self, data, code):
		if code == 404: return 'HTTP/1.1 404 Not found\n\n'.encode() + data.encode()

		elif code == 405: return 'HTTP/1.1 405 Method not allowed\n\n'.encode() + data.encode()

		elif code == 502: return 'HTTP/1.1 502 Bad gateway\n\n'.encode() + data.encode()

		else: return 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\n'.encode() + data.encode()

	def __decode_url(self, url):
		return urllib.parse.unquote(url)

	def __parse_request(self, data):
		parsed_datas = {'unk': []}

		data_list_line = data.split('\n')

		for line in data_list_line[1:]:
			try:
				parsed_datas[line.split(': ')[0]] = line.split(': ')[1]
			except:
				parsed_datas['unk'].append(line)

		return parsed_datas


	def __print(self, data, time=False, status='log'):
		str_to_print = ''

		if time:
			str_to_print += f'[{str(datetime.now())[:-7]}] '

		str_to_print += str(data)

		if status == 'log':
			print(Fore.GREEN + f'[LOG] {str_to_print}')

		elif status == 'warning':
			print(Fore.YELLOW + f'[WARNING] {str_to_print}')

		elif status == 'error':
			print(Fore.RED + f'[ERROR] {str_to_print}')

		else:
			print(f'[INFO] {str_to_print}')


	def __create_card(self, pr, tit, des, l):
		return f'''<div style="float: left; margin: 1em; auto; display: flex; font-family: Nunito, sans-serif; width: 17em; box-shadow: 0 4px 8px rgba(0,0,0,0.05), 0 5px 5px rgba(0,0,0,0.05); border-radius: 10px; box-shadow: 0 0 0 3px rgb(240, 245, 230); text-indent: 30px; padding-left: 1em; padding: 0.7em;">
	<div style="margin-left: 0.8rm; margin-top: 0.4em;">
		<p style="font-weight: 600; font-size: 20px; line-height: 5; line-height: 24px; color: #C7A17A;"> {pr} </p>
		<h3 style="font-style: normal; font-weight: bold; font-size: 24px; line-height: 28px; color: #232C38; margin-top: 10px;"> {tit} </h3>
		<p style="font-weight: 300; font-size: 16px; line-height: 22px; color: #151D28; margin-top: 20px;"> {des} </p>
		<div style="margin-top: 25px; display: flex; justify-content: space-between;">
			<a class="toggle-buy" href="{l}"> MORE... </a>
		</div>
	</div>
</div>
'''


	def create_socket(self):
		self.MAIN_SERVER = socket.socket()

		port = self.__IP__[1]

		number_of_port = -1

		while True:
			try:
				self.__print(f'Binding server on {self.__IP__[0]}:{self.__IP__[1]}.')

				self.MAIN_SERVER.bind((self.__IP__[0], port))

				self.__IP__ = (self.__IP__[0], port)

				self.__print(f'Server has been binded on {self.__IP__[0]}:{self.__IP__[1]}.')

				self.MAIN_SERVER.listen()

				self.__print('Server has been started.')

				self.__print(f'Main link: http://{self.__IP__[0]}:{self.__IP__[1]}/help.html', status = None)

				self.host = f'http://{self.__IP__[0]}:{self.__IP__[1]}'

				time.sleep(1)

				break

			except:
				self.__print(f'Port {port} is bizzy.', status = 'error')

				number_of_port += 1

				if number_of_port >= len(self.stocks_ports):
					port = random.randint(1, 36256)
				else:
					port = self.stocks_ports[number_of_port]

				self.__print(f'Founded new port: {port}.')

				time.sleep(1)


	def client_func(self, client, client_ip):
		# self.__print(f'Client {client_ip[0]}:{client_ip[1]} has been connected.')

		try:
			data = client.recv(102400).decode('utf-8')
	
			parsed_datas = self.__parse_request(data)
	
	
			if data:

				data_list_line = data.split('\n')
		
				header = data_list_line[0].split(' ')
		
				method = header[0]

				if method == 'GET':

					file = header[1][1:]
		
					url = self.host + header[1]

					if file.split('?')[0] == 'forum.html' or file.split('?')[0] == 'forum':

						self.host = parsed_datas['Host'][:-1]

						forum_data = open(f'{self.main_path}\\templates\\forum.html').read()

						response = self.__create_responce(f'{self.send_message_form}<div style="float: left"><h2>Chat: </h2>{forum_data}</div></body>', 200)
	
						client.send(response)

						self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} went to {self.host}/forum.', time=True)

					elif file.split('?')[0] == 'notifboard' or file.split('?')[0] == 'notifboard.html':

						args_ = file

						try:
							price, title, description, link = [self.__decode_url(d.split('=')[1].replace('+', ' ')) for d in args_.split('?')[1].split('&')]

							del_words = ['<', '>']

							for DW in  del_words:
								if re.search(DW, price) or re.search(DW, title) or re.search(DW, description) or re.search(DW, link):
									response = self.__create_responce(f'<body style="background: rgb(0, 0, 0) ; color: rgb(183, 190, 187);">	<h1 style="font-size: 2.5em; text-align: left;">Dark Web</h1>	<h1 style="text-align: center; font-size: 5em;">[502] Uncorrect symvols!</h1></body>', 200)
									client.send(response)
	
									return 0


							cart = self.__create_card(price, title, description, link)

							file_data = open(f'{self.main_path}\\templates\\notifboard.html').read()


							if re.search(cart[:-1], file_data):
								file_data = open(f'{self.main_path}\\templates\\notifboard.html').read()
	
								response = self.__create_responce(f'{self.notifboard_temps[0]}<h1 style="font-size: 5em; text-align: center;">Cart has been alredy on the board.</h1>{self.notifboard_temps[1]}', 502)
			
								client.send(response)
	
								self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} went to {self.host}/notifboard.', time=True)

								return 0


							file_data = file_data.split('\n')


							if len(file_data) > 551:
								file_data = file_data[:-12]

							file_data.insert(0, cart)
							file_data = '\n'.join(file_data)


							if title == '' or description == '' or link == '':
								file_data = open(f'{self.main_path}\\templates\\notifboard.html').read()
	
								response = self.__create_responce(f'{self.notifboard_temps[0]}{file_data}{self.notifboard_temps[1]}', 200)
			
								client.send(response)
	
								self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} went to {self.host}/notifboard.', time=True)

								return 0


							open(f'{self.main_path}\\templates\\notifboard.html', 'w').write(file_data)

							response = self.__create_responce(f'{self.notifboard_temps[0]}{file_data}{self.notifboard_temps[1]}', 200)
		
							client.send(response)

							self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} send notification in {self.host}/notifboard.', time=True)
						except:
							file_data = open(f'{self.main_path}\\templates\\notifboard.html').read()

							response = self.__create_responce(f'{self.notifboard_temps[0]}{file_data}{self.notifboard_temps[1]}', 200)
		
							client.send(response)

							self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} went to {self.host}/notifboard.', time=True)


					elif file.split('?')[0] == 'forum_send.html' or file.split('?')[0] == 'forum_send':
						args_ = file

						nicname, message = args_.split('?')[1].split('&')

						nicname = self.__decode_url(nicname.split('=')[1].replace('+', ' '))
						message = self.__decode_url(message.split('=')[1].replace('+', ' '))

						del_words = ['<', '>']

						for DW in  del_words:
							if re.search(DW, nicname) or re.search(DW, message):
								response = self.__create_responce(f'<body style="background: rgb(0, 0, 0) ; color: rgb(183, 190, 187);">	<h1 style="font-size: 2.5em; text-align: left;">Dark Web</h1>	<h1 style="text-align: center; font-size: 5em;">[502] Uncorrect symvols in your nicname or message!</h1></body>', 200)
								client.send(response)

								return 0

						if nicname == '' or message == '':
							forum_data = open(f'{self.main_path}\\templates\\forum.html').read()

							response = self.__create_responce(f'{self.send_message_form}<div style="float: left"><h2>Chat: </h2>{forum_data}</div></body>', 200)
		
							client.send(response)

							return 0


						forum_data = open(f'{self.main_path}\\templates\\forum.html').readlines()
		
						forum_data.insert(0, f'[{str(datetime.now())[:-7]}] {nicname}  {message}<br>')
		
						if len(forum_data) > 20:
							forum_data = forum_data[:-1]
		
						forum_data = ''.join(forum_data)
		
						open(f'{self.main_path}\\templates\\forum.html', 'w').write(forum_data)

						response = self.__create_responce(f'<script>window.location.href = "/forum";</script>', 200)
						client.send(response)

						self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} send a message in {self.host}/forum.', time=True)

					else:
		
						self.__print(f' [GET] Client {client_ip[0]}:{client_ip[1]} went to {url}.', time = True)
	 		
						try:
							if file[-4:] != 'html':
								response = self.__create_responce('\n'.join('<br>'.join(self.templates[file].read().decode('utf-8').split('\n')).split('\n')[4:]), 200)
	
								self.templates[file] = open(self.main_path + f'\\templates\\{file}', 'rb')
				
							else:
								response = self.__create_responce(self.templates[file].read().decode('utf-8'), 200)
	
								self.templates[file] = open(self.main_path + f'\\templates\\{file}', 'rb')
	
						except:
							response = self.__create_responce(open(self.main_path + '\\templates\\page_not_found.html').read(), 404)
						finally:
							client.send(response)
	
				elif method == 'POST':
					while True:

						if not re.search('WebKitFormBoundary', data.split('\n')[-2]):
							data += client.recv(102400).decode('utf-8')
						else:
							break

					parsed_datas = self.__parse_request(data)


					file_info = parsed_datas['Content-Disposition']

					file_type, file_name = file_info.split('; ')[1:]

					file_type = file_type[6:-1]
					file_name = file_name[10:-2]

					file_data = '\n'.join(data.split('Content-Type')[2].split('\n')[1:-3])


					bd_with_base_pages1 = ['forum', 'forum_send', 'notifboard']
					bd_with_base_pages2 = [host + '.html' for host in bd_with_base_pages1]


					try:
						if file_name not in bd_with_base_pages1 or file_name not in bd_with_base_pages2:
							open(f'{self.main_path}\\templates\\{file_name}', 'rb')

						response = self.__create_responce('<body style="background: rgb(0, 0, 0) ; color: rgb(183, 190, 187);"><h1 style="font-size: 2.5em; text-align: left;">Dark Web</h1><div style="text-align: center"><h1>File hasn`t been saved in Dark Web.</h1><br><hr><br><p>File has already in the Web, so you can not upload it again.</p></div></body>', 200)

						client.send(response)
					except:
						open(f'{self.main_path}\\templates\\{file_name}', 'wb').write(file_data.encode())

						self.templates[file_name] = open(f'{self.main_path}\\templates\\{file_name}', 'rb')
	
						try:
							response = self.__create_responce(f'<h1>{file_name}</h1>' + '<br>'.join(file_data.split('\n')), 200)
					
							client.send(response)
						except:
							response = self.__create_responce(open(self.main_path + '\\templates\\page_not_found.html').read(), 404)
	
							client.send(response)
	
						self.__print(f'[POST] Client {client_ip[0]}:{client_ip[1]} went to {parsed_datas["Referer"]};\nFile has been getted; Type: {file_type}; Name: {file_name}; Size: {len(file_data)}', time = True)
	
	
				else:
					response = self.__create_responce('<h1>Uncorrect method!</h1>', 405)
	
					client.send(response)
		except Exception as error:
			response = self.__create_responce(f'<h1>Error in getting data:</h1><br><p>{error}</p>', 500)
	
			client.send(response)

			self.__print(f'Error ({client_ip}): {error}', status = 'error')


	def main(self):
		while True:

			client, client_ip = self.MAIN_SERVER.accept()

			threading.Thread(target=self.client_func, args=(client, client_ip)).start()


	def start(self):
		self.create_socket()

		self.main()


if __name__ == '__main__':
	s = Main('127.0.0.1', port = 90)

	s.start()
