class MySet:
    def __init__(self):
        self.pathsInSet = {}

    def addToSet(self, path):
        if path not in self.pathsInSet.keys():
            self.pathsInSet[path] = path


    def intersection(self, other):
        resultSet = MySet()
        for path in self.pathsInSet.keys():
            if path in other.pathsInSet.keys():
                resultSet.addToSet(path)


        return resultSet


    def union(self, other):
        resultSet = MySet() # rezultat je nova instanca
        for p in self.pathsInSet.keys():
            resultSet.addToSet(p)
        for p in other.pathsInSet.keys():
            resultSet.addToSet(p)
        return resultSet


    def complement(self, other):
        resultSet = MySet()
        for p in self.pathsInSet.keys():
            if p not in other.pathsInSet.keys():
                resultSet.addToSet(p)
        return resultSet


    def removePath(self, path):
        if path in self.pathsInSet.keys():
                self.pathsInSet.pop(path)
        return self