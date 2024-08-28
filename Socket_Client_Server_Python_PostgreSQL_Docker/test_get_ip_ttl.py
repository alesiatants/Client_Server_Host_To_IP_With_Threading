import unittest
from ping_ip_ttl import get_ip_ttl

class TestGetIpTtl(unittest.TestCase):
    
    def test_get_ip_ttl_valid_domain(self):
        '''Проверка корректности типов данных, возвращаемых при получении ip и ttl при правильно введенном домене'''
        ttl, ip = get_ip_ttl("google.com")
        self.assertIsInstance(ttl, int)
        self.assertIsInstance(ip, str)

    def test_get_ip_ttl_domain_with_spaces(self):
        '''Проверка корректности типов данных, возвращаемых при получении ip и ttl при правильно домене с пробелами'''
        ttl, ip = get_ip_ttl("example . com")
        self.assertIsInstance(ttl, int)
        self.assertIsInstance(ip, str)
        
    def test_get_ip_ttl_invalid_domain(self):
        '''Проверка корректности типов данных, возвращаемых при получении ip и ttl при неправильно введенном домене'''
        result = get_ip_ttl("invalid_domain")
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
