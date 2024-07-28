import socket
import time

def create_client(host, port):
	'''Функция создает потоковый сокет клиента, отправляет/принимает сообщение от серевера'''

	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Ожидание соединения')
	connected = False
	while not connected:
		try:
			ClientSocket.connect((host, port))
			connected = True
		except socket.timeout as er:
			print(f"Долгое ожидание, пытаемся переподключиться - {er}")
			time.sleep(5)  # Ждем 5 секунд перед повторной попыткой
		except ConnectionRefusedError as ex:
			print(f"Ошибка соединения - {ex}")
			exit(1)
	work_with_server(ClientSocket)
	 
def work_with_server(ClientSocket):
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
			print(f"Соединение остановлено, сервер закончил работу - {ex}")
			break
		try:
		# Получение данных в двоичном формате от сервера с установкой макс. колич. байтов в сообщении
			data = ClientSocket.recv(1024)
		except ConnectionResetError as ex:
			print(f"Соединение остановлено, сервер закончил работу - {ex}")
			break

		answer = data.decode()
		print(f'Получено:\n{answer}') 

def main():
	'''Запускает клиента на localhost:10000'''
	create_client('localhost', 10000)

if __name__=='__main__':
	main()

