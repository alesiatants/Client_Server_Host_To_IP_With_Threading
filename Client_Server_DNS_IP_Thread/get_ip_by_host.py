import socket

def get_ip_by_hostname(hostname):
	'''Функция преобразования имени домена в формат адреса IPv4, при наличии множества 
	соответствующих ip - выводит их в виде списка'''
	try:
		return f'Домен - {hostname}\nIP адрес:\n'+"\n".join([f'{ip}' for ip in socket.gethostbyname_ex(hostname)[2:][0]])
	except socket.gaierror as er:
		# При отсутствии введенного домена или неправильном вводе запроса со стороны клиента
		# выводится соответствующая проблема
		return f'Домен не валиден - {er}'
	
 

