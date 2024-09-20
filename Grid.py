  
    
class Grid():
    def __init__(self, taillex, tailley):
        self.sizeX = taillex
        self.sizeY = tailley
        self.grille = [[Cellule(x, y) for x in range(taillex)] for y in range(tailley)]

    def __repr__(self):
        txt = ""
        nbespaces = 0
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                txt += str(self.getGrille()[y][x])
                nbespaces = 3 - len(str(self.getCellule(y, x)))
                txt += " "*nbespaces
                txt += "    "
            txt += '\n'
        return txt

    def sortie(self, x, y):
        return (x < 0 or y < 0 or x > self.maxX() or y > self.maxY())

    def getGrille(self):
        return self.grille

    def getRow(self, y):
        return self.grille[y]

    def getColumn(self, x):
        return self.grille[x]

    def getCellule(self, y, x):
        if (self.sortie(x, y)):
            return None
        
        return self.grille[y][x]

    def getSizeX(self):
        return self.sizeX

    def getSizeY(self):
        return self.sizeY

    def maxX(self):
        return (self.sizeX - 1)

    def maxY(self):
        return (self.sizeY - 1)


class Cellule():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.voisins = []

    def __repr__(self):
        return "(" + str(self.y) + ", " + str(self.x) + ")"

    def chercheVoisins(self, grid):
        grille = grid.getGrille()
        if self.getX() > 0:
            self.voisins.append(grille[self.y][self.x - 1])

        if self.getX() < grid.maxX():
            self.voisins.append(grille[self.y][self.x + 1])

        if self.getY() > 0:
            self.voisins.append(grille[self.y - 1][self.x])

        if self.getY() < grid.maxY():
            self.voisins.append(grille[self.y + 1][self.x])
            
    def getX(self):
        return self.x

    def getY(self):
        return self.y


class GameGrid(Grid):
    def __init__(self, tx, ty):
        super().__init__(tx, ty)
        self.grille = [[GameCell(x, y) for x in range(tx)] for y in range(ty)]

    def areAllLakes(self, cells):
        for c in cells:
            if c is None:
                return False

            if not c.isLake():
                return False

        return True

        
class GameCell(Cellule):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = 0
        self.locked = False
        self.isleValue = -1

    def isLake(self):
        return (self.state == 1)

    def isIsle(self):
        return (self.state == 0)

    def isIsolatedIsle(self):
        if self.isLake():
            return False
        
        for v in self.voisins:
            if (v.isIsle()):
                return False

        return True

    def toIsle(self):
        self.state = 0

    def toLake(self):
        self.state = 1

    def changeState(self):
        if not self.locked:
            self.state += 1
            self.state %= 2

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
