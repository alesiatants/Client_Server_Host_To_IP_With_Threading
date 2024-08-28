import unittest
from unittest.mock import MagicMock
from threading import Lock
from queue import Queue
import threading
from server import refreshsufixtree, SuffixTree

class TestRefreshSufixtree(unittest.TestCase):
    
    def setUp(self):
        # Создаем мок-объект для подключения к базе данных
        self.mock_conn = MagicMock()
        # Настраиваем метод select_all, чтобы возвращать предопределенные данные
        self.mock_conn.select_all.return_value = [
            ('example.com', '93.184.216.34'),
            ('test.com', '192.0.2.1')
        ]
        # Создаем блокировку для использования в тесте
        self.lock = Lock()
        # Создаем очередь для передачи данных из потока
        self.result_queue = Queue()

    def test_refreshsufixtree(self):
        '''Проверка, что при наличии строк в БД, они фиксируются в дереве суффиксов'''
        # Запускаем refreshsufixtree в отдельном потоке
        test_thread = threading.Thread(target=refreshsufixtree, args=(self.lock, self.mock_conn, self.result_queue))
        test_thread.start()

        # Даем функции немного времени для выполнения
        test_thread.join(timeout=11)

        # Получаем результат из очереди
        self.suffixtree = self.result_queue.get()

        # Проверяем, что в suffixtree есть ожидаемые данные
        self.assertIsNotNone(self.suffixtree, "SuffixTree не был создан.")
        self.assertIsInstance(self.suffixtree, SuffixTree)

        expected_values = [
            ('example.com', '93.184.216.34'),
            ('test.com', '192.0.2.1')
        ]
        for key, value in expected_values:
            results = self.suffixtree.search_substring(key)
            self.assertIn((key, value), results)

        # Проверяем, что метод select_all был вызван
        self.mock_conn.select_all.assert_called()

if __name__ == '__main__':
    unittest.main()
