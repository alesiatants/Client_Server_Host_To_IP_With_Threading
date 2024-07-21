import socket

def create_client(host, port):
	'''Функция создает потоковый сокет клиента, отправляет/принимает сообщение от серевера'''
	
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Ожидание соединения')

	try:
		ClientSocket.connect((host, port))
	except socket.error as e:
		print(str(e))

	while True:
		print('Для завершения сеанса введите q+↩️')
		question = input("Введите название хоста: ")

		while not question:
			print("Введенная строка пустая!")
			question = input("Введите название хоста: ")

		# Условие завершения сеанса
		if question=="q":
			print('Закрываем сокет')
			quit = "Выход".encode()
			ClientSocket.sendall(quit)
			ClientSocket.close()
			break

		print(f'Отправка: {question}')
		ques = question.encode()

		try:
		# Отправка данных запроса серверу в двоичном формате
			ClientSocket.sendall(ques)
		except Exception as ex:
			print("Соединение остановлено")
			break

		# Получение данных в двоичном формате от сервера с установкой макс. колич. байтов в сообщении
		data = ClientSocket.recv(1024)

		if(data.decode()=="0"):
			print("Некорректные данные")
			continue
		
		answer = data.decode()
		print(f'Получено:\n{answer}') 


def main():
	'''Запускает клиента на localhost:10000'''
	create_client('localhost', 10000)

if __name__=='__main__':
	main()


