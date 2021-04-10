class Node:

    def __init__(self, parent):
        self.parent = parent
        self.token = None
        self.children = []

    def setToken(self, token):
        self.token = token

    def addChild(self, node):
        self.children.append(node)

    # NAREDNE DVE METODE SLUZE SAMO ZA LEP ISPIS STABLA NA KONZOLU, I NADJENE SU NA STACK-U
    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        # sta ako cvor nema decu
        if len(self.children) == 0:
            line = '%s' % self.token
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # sta ako ima samo jedno dete
        if len(self.children) == 1:
            lines, n, p, x = (self.children[0])._display_aux()
            s = '%s' % self.token
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # sta ako ima oba deteta
        left, n, p, x = self.children[0]._display_aux()
        right, m, q, y = self.children[1]._display_aux()
        s = '%s' % self.token
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def parsirajKomandu(komanda):
    tokeni = []
    temp_string = ''
    i = 0
    while i < len(komanda):
        if komanda[i] == ' ':
            if temp_string != '':
                tokeni.append(temp_string)
                temp_string = ''
        elif komanda[i] == '!':
            if temp_string != '':
                tokeni.append(temp_string)
                temp_string = ''
            tokeni.append('!')
        elif komanda[i] == '(':
            if temp_string != '':
                tokeni.append(temp_string)
                temp_string = ''
            tokeni.append('(')
        elif komanda[i] == ')':
            if temp_string != '':
                tokeni.append(temp_string)
                temp_string = ''
            tokeni.append(')')
        elif komanda[i] == '&':
            if komanda[i + 1] == '&':
                if temp_string != '':
                    tokeni.append(temp_string)
                    temp_string = ''
                tokeni.append('&&')
                i += 1
            else:
                print('GRESKA: karakter \'&\' moze da se koristi iskljucivo u operatoru && i ne moze da se nadje ni u '
                      'kom drugom kontekstu')
        elif komanda[i] == '|':
            if komanda[i+1] == '|':
                if temp_string != '':
                    tokeni.append(temp_string)
                    temp_string = ''
                tokeni.append('||')
                i += 1
            else:
                print('GRESKA: karakter \'|\' moze da se koristi iskljucivo u operatoru || i ne moze da se nadje ni u '
                      'kom drugom kontekstu')
        else:
            temp_string += komanda[i]
        i += 1
    if temp_string != '':
        tokeni.append(temp_string)
    if tokeni.count('(') != tokeni.count(')'):
        print('Broj otvorenih zagrada i zatvorenih zagrada mora biti jednak')
    rootNode = konstruisiStabloOdTokena(tokeni, 0)
    rootNode.display()


def konstruisiStabloOdTokena(tokeni, currentToken):
    rootNode = Node(None)
    currentNode = rootNode

    i = currentToken
    while i < len(tokeni):
        token = tokeni[i]
        if token == '!':
            if i+1 == len(tokeni) or tokeni[i+1] in ['||', '&&']:
                print('Nakon operatora ! ne smeju da stoje operatiro || ili &&, i operaton ! ne sme da bude kraj izraza')
                return None
            currentNode.setToken('!')
            currentNode.addChild(Node(currentNode))
            currentNode = currentNode.children[-1]
        elif token == '||':
            newRootNode = Node(None)
            newRootNode.token = '||'
            newRootNode.children.append(rootNode)
            rootNode.parent = newRootNode
            rootNode = newRootNode
            currentNode = Node(rootNode)
            rootNode.children.append(currentNode)
        elif token == '&&':
            newRootNode = Node(None)
            newRootNode.token = '&&'
            newRootNode.children.append(rootNode)
            rootNode.parent = newRootNode
            rootNode = newRootNode
            currentNode = Node(rootNode)
            rootNode.children.append(currentNode)
        elif token == '(':
            returnedRootNode, i = konstruisiStabloOdTokena(tokeni, i+1)
            currentNode.children = returnedRootNode.children
            currentNode.token = returnedRootNode.token
        elif token == ')':
            return rootNode, i
        else:
            currentNode.token = token
        i += 1
    return rootNode


if __name__ == '__main__':
    parsirajKomandu("!rec && !(juce || (danas && kadgod)) || ajde && (!radi || kraj)")
