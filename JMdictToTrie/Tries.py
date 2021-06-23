class TextTrieNode:
 
    def __init__(self, char):
        self.char = char
        self.value = None
        self.is_end = False
        self.children = {}

class IdTrieNode:
 
    def __init__(self, char):
        self.char = char
        self.value = None
        self.is_end = False
        self.children = {}
 
class IdTrie(object):
 
    def __init__(self):
        self.root = IdTrieNode("")
     
    def insert(self, word, value):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = IdTrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.is_end = True
        node.value = value
         
    def search(self, x):
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return node.value

class TextTrie(object):
    def __init__(self):
        self.root = TextTrieNode("")
     
    def insert(self, word, value):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TextTrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        node.is_end = True
        node.value = value
         
    def search(self, x):
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return node.value