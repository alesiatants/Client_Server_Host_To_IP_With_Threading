import socket
# импорт модуля с методом поиска ip адреса по введенному хосту
from get_ip_by_host import get_ip_by_hostname
# импорт библиотеки для работы с потоками и управлением многопоточностью
from _thread import * 


def create_server(host, port):
	'''Функция создает потоковый сокет сервера и оперирует соединениями с клиентами'''
	# Создаем потоковый (TCP/IP) сокет сервера
	ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Установка начального количества задействованных потоков
	ThreadCount = 0
	try:
		# Установка соединения клиента с сервером по порту
		ServerSocket.bind((host, port))
	except socket.error as e:
		# Отслеживание ошибки при установки соединения
		print(str(e))

	print('Ожидание соединения...')
	# Перевод сервера в режим приема соединений в размере 10000 клиентов
	ServerSocket.listen(10000)

	def threaded_client(connection):
		'''Функция, которая обрабатывает запросы от отдельных клиентов в потоке и которая 
		подключается к каждому клиенту по другому адресу, указанному сервером'''
		while True:
			# Получение данных запроса от клиента с макс колич. байтов 1024 в сообщении
			data = connection.recv(1024)
			print(f'Получен домен: {data.decode()}')
			if not data:
				break
			print('Обработка данных...')
			res = get_ip_by_hostname(data.decode())
			print('Отправка обратно клиенту.')
			# Отправка обработанных данных клиенту
			connection.sendall(res.encode())
		connection.close()

	while True:	
		# Принимаем соединение от клиента с помощью accept(), 
		# возвращающим тип клиента, который подключился, а также 
		# предоставленный ему уникальный номер потока или адрес
		object_conn, address = ServerSocket.accept()
		print('Установлено соединение с: ' + address[0] + ':' + str(address[1]))
		# Функция класса потока start_new_thread()
		# создает/назначает новый поток каждому клиенту для 
		# индивидуальной обработки
		start_new_thread(threaded_client, (object_conn, ))
		# Установка количества задействованных потоков
		ThreadCount += 1
		print('Номер потока: ' + str(ThreadCount))
	ServerSocket.close()


def main():
	'''Основная функция, вызывающая создание потокового сокета сервера,
	функционирующего на порту 10000 и ip адресе localhost (127.0.0.1)'''
	create_server('localhost', 10000)

if __name__=='__main__':
	main()