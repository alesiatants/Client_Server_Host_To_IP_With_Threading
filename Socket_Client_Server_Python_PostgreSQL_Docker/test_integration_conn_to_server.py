import unittest
from server import check_db_dns
from connection import Connection

class TestServerConnectionIntegration(unittest.TestCase):
    
    def setUp(self):
        self.conn = Connection()

    def test_check_db_dns_integration(self):
        '''Проверка, что возвращает функция'''
        result = check_db_dns(self.conn, "example.com")
        self.assertIsInstance(result, str)  # Проверка, что результат - строка (IP адрес)
    def test_check_db_dns_integration_erroedata(self):
        '''Проверка на правильную обработку некорректного домена'''
        result = check_db_dns(self.conn, "fbvjfjvbjfbjb")
        self.assertEqual(result, "Некорректные данные")
				
if __name__ == '__main__':
    unittest.main()
