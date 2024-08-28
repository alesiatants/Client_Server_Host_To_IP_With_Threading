import unittest
import socket
import threading
import time
from queue import Queue
from server import create_server
from client import create_client
from connection import Connection
from ping_ip_ttl import get_ip_ttl

class EndToEndTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''Настройка сервера и клиента'''
        # Запуск сервера в отдельном потоке
        cls.server_thread = threading.Thread(target=create_server, args=('localhost', 10000))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Даем серверу немного времени для запуска
        time.sleep(2)
        
        # Создаем клиента
        cls.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.client_socket.connect(('localhost', 10000))

    @classmethod
    def tearDownClass(cls):
        '''Закрытие соединений'''
        cls.client_socket.close()

    def test_add_and_find_domain(self):
        '''Проверка добавления и поиска домена'''
        domain = "example.com"
        ip = get_ip_ttl(domain)[1]  # Получаем IP-адрес для тестируемого домена
        query = f"{domain}"
        
        # Отправляем запрос на добавление домена
        self.client_socket.sendall(query.encode())
        response = self.client_socket.recv(1024).decode()
        
        # Проверяем, что сервер ответил корректно
        self.assertIn(ip, response)
        
        # Ждем, пока обновится дерево суффиксов
        time.sleep(12)  # Даем время для обновления данных в сервере
        
        # Отправляем запрос на поиск домена
        query = f"find {domain}"
        self.client_socket.sendall(query.encode())
        response = self.client_socket.recv(1024).decode()
        
        # Проверяем, что сервер возвращает корректный IP-адрес
        self.assertIn(f"{domain}: {ip}", response)

if __name__ == '__main__':
    unittest.main()
