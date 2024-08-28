import unittest
import time
from threading import Lock, Thread
from server import cleanup

class TestCleanup(unittest.TestCase):
    
    def setUp(self):
        self.lock = Lock()
        self.table = {"old_domain": ("192.168.1.3", time.time() - 10)}
    
    def test_cleanup(self):
        '''Проверка, действует ли очистка при добавлении застаревших доменов'''
        # Создаем и запускаем поток для выполнения функции cleanup
        cleanup_thread = Thread(target=cleanup, args=(self.lock, self.table))
        cleanup_thread.daemon = True  # Делаем поток демоном, чтобы он не блокировал завершение теста
        cleanup_thread.start()
        
        # Ждем некоторое время, чтобы дать функции cleanup время для выполнения
        time.sleep(11)  
        
        # Проверяем результат очистки
        self.assertEqual(len(self.table), 0)
        

if __name__ == '__main__':
    unittest.main()
