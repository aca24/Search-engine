class TrieNode:
    def __init__(self, parent=None, char=None, htmlFile=None): # konstruktor
        self.char = char # jedan karakter
        if self.char is not None: # ako postoji karakter
            self.char = self.char.lower()
        self.parent = parent
        self.children = [] # deca
        self.end = False # kraj
        self.counter = 0 # brojac
        self.htmlFile = htmlFile
        self.myDict = {}  # recnik - kljuc: putanja, vrednost: broj ponavaljanja

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insertWord(self, word, htmlFile):
        node = self.root # krece od pocetka, postavlja da je to koren
        word = word.lower()
        for char in word: # prolazi kroz svaki karakter u prosledjenoj reci
            foundInChild = False
            for child in node.children: # prolazi kroz svu decu za trenutni cvor, prvo je root, a kasnije se menja
                if child.char == char: # ako trenutni karakter = kao karakter koji ima to dete
                    node = child
                    foundInChild = True
                    break
            if not foundInChild:
                new = TrieNode(node, char, htmlFile)
                node.children.append(new)
                node = new

        node.end = True

        if node.htmlFile != htmlFile: # ako se razlikuju trenutni i poslati html fajl
            if node.counter != 0: # ukoliko ima ponavljanja napuni recnik
                node.myDict[node.htmlFile] = node.counter # punjenje recnika
            node.counter = 1 # resetujem broj ponavljanja reci na 1
            node.htmlFile = htmlFile # trenutni html fajl stavljam na poslati html fajl
        elif node.htmlFile == htmlFile: # ukoliko su isti fajlovi
                node.counter += 1 # broj ponavljanja reci se povecava za jedan

    def search(self, word):
        word = word.lower().strip() # case insensitive search
        node = self.root  # postavljam pocenti cvor

        if len(node.children) == 0:
            return False, 0, {}, None # ukoliko nema decu odmah vracam gresku

        for char in word: # prolazak kroz svaki karakter za poslatu rec
            charNotFound = True # na pocetku nije pronadjena
            for child in node.children: # prolazak kroz svu decu
                if child.char == char: # ako su isti, pronasao je
                    charNotFound = False
                    node = child # postavljanje novog cvora
                    break
            if charNotFound: # ukoliko nije pronasao
                return False, 0, {}, None

        if node.end == False: # ukoliko nije dodao tu rec
            return False, 0, {}, None

        return node.end, node.counter,  node.myDict, node.htmlFile
        # povratna vrednost: da li rec postoji, broj ponavljanja te reci, recnik, putanja tj. html fajl
