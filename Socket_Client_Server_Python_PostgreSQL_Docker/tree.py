from collections import defaultdict

# Реализация суффиксного дерева
class SuffixTreeNode:
    def __init__(self):
        self.children = defaultdict(SuffixTreeNode)
        self.is_end_of_key = False
        self.values = []

class SuffixTree:
    def __init__(self):
        self.root = SuffixTreeNode()

    def insert(self, key: str, value):
        """Вставляет ключ в дерево с соответствующим значением, разбивая символы ключа на узлы."""
        current = self.root
        for char in key:
            current = current.children[char]
        current.is_end_of_key = True
        if (key, value) not in current.values:
            current.values.append((key, value))

    def search_substring(self, substring: str) -> list:
        """Ищет подстроку в любом месте ключа и возвращает список пар (ключ, значение)."""
        result = []
        self._search_from_all_nodes(self.root, substring, "", result)
        return result

    def _search_from_all_nodes(self, node: SuffixTreeNode, substring: str, path: str, result: list):
        """Рекурсивно ищет подстроку в любом месте ключа."""
        # Проверяем, содержит ли текущий путь подстроку
        if substring in path:
            result.extend((path, value) for _, value in node.values)

        # Рекурсивно ищем по всем дочерним узлам
        for char, child in node.children.items():
            self._search_from_all_nodes(child, substring, path + char, result)


