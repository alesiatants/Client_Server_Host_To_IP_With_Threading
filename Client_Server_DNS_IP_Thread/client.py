import socket

def create_client(host, port):
	'''Функция создает потоковый сокет клиента и оперирует сессией клиента, общением с сервером'''
	# Создаем потоковый (TCP/IP) сокет клиента
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print('Ожидание соединения')
	try:
		# Установка соединения клиента с сервером по порту
		ClientSocket.connect((host, port))
	# Отслеживание ошибки при установки соединения
	except socket.error as e:
		print(str(e))

	while True:
		print('Для завершения сеанса введите q+↩️')
		question = input("Введите название хоста: ")
		# Условие завершения сеанса
		if question=="q":
			print('Закрываем сокет')
			ClientSocket.close()
			break

		print(f'Отправка: {question}')
		# Конвертация данных запроса в двоичный формат
		ques = question.encode()
		# Отправка данных запроса серверу в двоичном формате
		ClientSocket.sendall(ques)
		# Получение данных в двоичном формате от сервера с установкой макс. колич. байтов в сообщении
		data = ClientSocket.recv(1024)
		# Конвертация данных ответа из двоичного формата в читабельный
		answer = data.decode()
		print(f'Получено:\n{answer}') 


def main():
	'''Основная функция, вызывающая создание потокового сокета клиента,
	функционирующего на порту 10000 и ip адресе localhost (127.0.0.1)'''
	create_client('localhost', 10000)

if __name__=='__main__':
	main()


