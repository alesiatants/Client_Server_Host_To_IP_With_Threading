import unittest
from tree import SuffixTree

class TestSuffixTree(unittest.TestCase):
    
    def setUp(self):
        self.tree = SuffixTree()

    def test_insert_strstart_and_search(self):
        '''Проверка на корректный поиск в дереве по первой половине строки с доменом'''
        self.tree.insert("example.com", "192.168.1.1")
        result = self.tree.search_substring("ex")
        self.assertEqual(result, [("example.com", "192.168.1.1")])
        
    def test_insert_strmiddle_and_search(self):
        '''Проверка на корректный поиск в дереве по средней части строки с доменом'''
        self.tree.insert("example.com", "192.168.1.1")
        result = self.tree.search_substring("ample.")
        self.assertEqual(result, [("example.com", "192.168.1.1")])
        
    def test_insert_strend_and_search(self):
        '''Проверка на корректный поиск в дереве по концовке строки с доменом'''
        self.tree.insert("example.com", "192.168.1.1")
        result = self.tree.search_substring(".com")
        self.assertEqual(result, [("example.com", "192.168.1.1")])
        
    def test_search_no_contained_data(self):
        '''Проверка реакции на невнесенную информацию в дерево'''
        result = self.tree.search_substring("nodata")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
