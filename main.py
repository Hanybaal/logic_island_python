from Grid import *
from Graphism import *
import os
import ctypes
import tkinter as tk
import math


#TODO
# Supprimer les îles de 1 touchés en diagonale à la génération en 1 grignotage

class Main():
    def __init__(self):
        usr32 = ctypes.windll.user32
        self.size1 = usr32.GetSystemMetrics(0)
        self.size2 = usr32.GetSystemMetrics(1)

        self.fen = tk.Tk()

        self.fen.attributes('-fullscreen', True)
        self.fen.maxsize(self.size1, self.size2)
        self.fen.minsize(self.size1, self.size2)
        self.fen.bind('<Key>', self.keyboardEvents)
        self.can = tk.Canvas(self.fen, bg = "aquamarine", height = self.size2,
                              width = self.size1)
        self.can.pack(side = tk.LEFT)

        self.coef = 10
        self.grid = GameGrid(self.coef, self.coef)
        for i in range(self.grid.getSizeY()):
            for j in range(self.grid.getSizeX()):
                self.grid.getCellule(i, j).chercheVoisins(self.grid)

        blankGrid = list(self.grid.getGrille())

        n = 3 if self.coef > 7 else 10
        self.getBestIsland(n)
        
        self.allIsles = []
        self.allSizes = []
        #On obtient une liste de listes de GameCell. Chaque liste correspond à une île
        self.getAllIsles()
        self.oneIsle()
        
        self.G = Graphism(self)
        self.G.getGraphism()
        self.getSizeAllIsles()

        #Pour quand on est en jeu
        self.allWholes = []

        self.fen.mainloop()

    def verifications(self):
        winCondition = True
        
        #Vérification des tailles des îles
        #Vérification des trous d'eau
        #Indication de victoire et lock de toutes les cases dans ce cas
        for i in range(self.grid.getSizeY()):
            for j in range(self.grid.getSizeX()):
                cell = self.grid.getCellule(i, j)

                if cell.isLake():
                    c1 = self.grid.getCellule(i + 1, j)
                    c2 = self.grid.getCellule(i, j + 1)
                    c3 = self.grid.getCellule(i + 1, j + 1)

                    if (self.grid.areAllLakes([c1, c2, c3])):
                        self.allWholes.append([cell, c1, c2, c3])
                        winCondition = False

                    else:
                        if cell is not None:
                            self.can.itemconfigure(
                                self.G.graphicalGrid[cell.getY()][cell.getX()],
                                fill = self.G.getColor(cell),
                                outline = self.G.getColor(cell))

                        if c1 is not None:
                            self.can.itemconfigure(
                                self.G.graphicalGrid[c1.getY()][c1.getX()],
                                fill = self.G.getColor(c1),
                                outline = self.G.getColor(c1))

                        if c2 is not None:
                            self.can.itemconfigure(
                                self.G.graphicalGrid[c2.getY()][c2.getX()],
                                fill = self.G.getColor(c2),
                                outline = self.G.getColor(c2))

                        if c3 is not None:
                            self.can.itemconfigure(
                                self.G.graphicalGrid[c3.getY()][c3.getX()],
                                fill = self.G.getColor(c3),
                                outline = self.G.getColor(c3))

                else:
                    #On est sur un centre d'île
                    if (cell.isleValue != -1):
                        vus = []
                        self.getIsle(cell, vus)
                        if (len(vus) != cell.isleValue):
                            winCondition = False

        for w in self.allWholes:
            for whole in w:
                self.can.itemconfigure(self.G.graphicalGrid[whole.getY()][whole.getX()],
                                       fill = "navy", outline = "navy")
        self.allWholes = []

        #Vérification de l'eau en 1 seul block
        nbWater = self.countWater()
        i, j = 0, 0
        while (i < self.grid.getSizeY() and winCondition):
            j = 0
            while (j < self.grid.getSizeX() and winCondition):
                cell = self.grid.getCellule(i, j)
                if (cell.isLake()):
                    vus = []
                    self.getIsle(cell, vus, False)
                    winCondition = (len(vus) == nbWater)
                    j += self.grid.getSizeX()
                    i += self.grid.getSizeY()
                    
                j += 1

            i += 1
                
        if winCondition:
            self.can.create_text(self.G.pax, self.G.pay,
                                 text = "Gagné!!",
                                 font = ('Georgia 15 bold'))
            for lig in self.grid.getGrille():
                for cell in lig:
                    cell.lock()
                
        return winCondition

    def countWater(self):
        total = 0
        for i in range(self.grid.getSizeY()):
            for j in range(self.grid.getSizeX()):
                if self.grid.getCellule(i, j).isLake():
                    total += 1
        return total
                

    def getSizeAllIsles(self):
        for isle in self.allIsles:
            size = len(isle)
            self.allSizes.append(size)
            aleaTerrain = isle[randint(0, size - 1)]
            aleaTerrain.lock()
            aleaTerrain.isleValue = size
            self.G.genereSizes(aleaTerrain, size)

    def oneIsle(self):
        for lig in self.grid.getGrille():
            for cell in lig:
                cell.toIsle()

    def getAllIsles(self):
        vus = []
        actualSize = 0
        ancientSize = 0
        for i in range(self.grid.getSizeY()):
            for j in range(self.grid.getSizeX()):
                cell = self.grid.getCellule(i, j)
                if not cell.isLake():
                    self.getIsle(cell, vus)

                actualSize = len(vus)
                #On a choppé une île
                if (actualSize > ancientSize):
                    self.allIsles.append(vus[(ancientSize - actualSize):])

                ancientSize = actualSize

    def getScore(self, island):
        score = 0
        vus = []
        ancientVus = []
        actualSize = 0
        ancientSize = 0
        
        for i in range(len(island)):
            for j in range(len(island[0])):
                cell = island[i][j]
                if not cell.isLake():
                    self.getIsle(cell, vus)
                    
                    actualSize = len(vus)
                    size = actualSize - ancientSize
                    if (size == 1):
                        score += 2

                    if (size > 9):
                        score += size - 9

                    ancientSize = actualSize
        
        return score

    def getBestIsland(self, n):
        #On génère n grilles et on prend la meilleure, avec le moins d'îles isolées
        #Et un minimum de grosses îles
        allIsles = []
        allScores = []
        for i in range(n):    
            self.genereGrid(int(math.exp(math.sqrt(self.coef + self.coef))))
            allIsles.append(list(self.grid.getGrille()))
            
            self.grid = GameGrid(self.coef, self.coef)
            for i in range(self.grid.getSizeY()):
                for j in range(self.grid.getSizeX()):
                    self.grid.getCellule(i, j).chercheVoisins(self.grid)

        for i in allIsles:
            allScores.append(self.getScore(i))

        self.grid.grille = allIsles[self.getMinScore(allScores)]

    def getMinScore(self, scores):
        mini = scores[0]
        index = 0
        for i in range(1, len(scores)):
            if (scores[i] < mini):
                mini = scores[i]
                mini = i
        return index
                

    def genereGrid(self, iles = 1):
        #1 choix case aléatoire sur un côté
        nbPas = self.coef*self.coef*self.coef
        alea = randint(1, 4)
        cello = None
        if (alea < 3):
            lig = (alea - 1 - 2*(alea > 3))*(self.grid.getSizeY() - 1)
            col = randint(0, self.grid.getSizeX() - 1)
            cello =  self.grid.getGrille()[lig][col]

        else:
            lig = randint(0, self.grid.getSizeY() - 1)
            col = (alea - 3)*(self.grid.getSizeX() - 1)
            cello = self.grid.getGrille()[lig][col]
        
        #2 Choix direction aléatoire (sans faire de trou d'eau) 
        #3 L'aléatoire pour la direction qui vient d'être prise est baissée
        #4 continue tant que pas assez d'îles
        poids = [25, 25, 25, 25]
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        indiceAlea = 0
        ancienIndiceAlea = -1
        alea -= 1
        while (self.ActualIslesNumber() < iles and nbPas):
            # Direction
            for i in range(len(directions)):
                newY, newX = (cello.getY() + directions[i][0],
                              cello.getX() + directions[i][1])

                    
                if self.grid.sortie(newY, newX):
                    poids[i] = 0

                else:
                    #Si ajouter le voisin fait un trou d'eau on oublie
                    nc = self.grid.getCellule(newY, newX)
                    if self.waterHole(nc):
                        poids[i] = 0

                    elif nc.isLake():
                        poids[i] = 0 if (poids[i] - 10 < 0) else (poids[i] - 10)

                    elif self.twoIsolatedIsles(nc):
                        poids[i] = 0

                    elif self.isolateIsle(nc):
                        poids[i] = 0 if (poids[i] - 15 < 0) else (poids[i] - 15)
                        

            s = sum(poids)
            nbAlea = randint(1, s)
            indiceAlea = 0
            for p in range(len(poids)):
                if sum(poids[:(p + 1)]) >= nbAlea:
                    indiceAlea = p
                    break

            #On a la direction indiceAlea
            newCell = self.grid.getCellule(cello.getY() + directions[indiceAlea][0],
                                           cello.getX() + directions[indiceAlea][1])
            cello = newCell
            if (not cello.isLake()):
                cello.changeState()
                

            #Pour finir on remet les poids         
            poids = [25, 25, 25, 25]
            poids[indiceAlea] -= 10

            if (indiceAlea == ancienIndiceAlea):
                poids[indiceAlea] -= 10

            if (indiceAlea%2):
                poids[indiceAlea - 1] -= 10

            else:
                poids[indiceAlea + 1] -= 10
                

            if (alea%2):
                poids[alea - 1] += 3

            else:
                poids[alea + 1] += 3

            ancienIndiceAlea = indiceAlea
            nbPas -= 1

    def isolateIsle(self, cell):
        #On vient de creuser de l'eau
        cell.changeState()
        for v in cell.voisins:
            if v.isIsolatedIsle():
                cell.changeState()
                return True

        cell.changeState()
        return False

    def twoIsolatedIsles(self, cell):
        #On vient de creuser de l'eau
        nbIsolatedIsles = 0

        cell.changeState()
        for v in cell.voisins:
            if v.isIsolatedIsle():
                nbIsolatedIsles += 1

        cell.changeState()
        return (nbIsolatedIsles > 1)

    def waterHole(self, cell):
        diags = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        for i in range(len(diags)):
            d = diags[i]
            if not self.grid.sortie(cell.getY() + d[0], cell.getX() + d[1]):
                if self.grid.getCellule(cell.getY() + d[0], cell.getX() + d[1]).isLake():
                    #On a possiblement un trou d'eau avec cette diagonale
                    if (self.grid.getCellule(cell.getY(), cell.getX() + d[1]).isLake()):
                        if (self.grid.getCellule(cell.getY() + d[0], cell.getX()).isLake()):
                            return True

        return False
    
    def ActualIslesNumber(self):
        vus = []
        nbIsles = 0
        
        for i in range(self.grid.getSizeY()):
            for j in range(self.grid.getSizeX()):
                cell = self.grid.getCellule(i, j)
                if (cell.isLake() or (cell in vus)):
                    pass

                else:
                    self.getIsle(cell, vus)
                    nbIsles += 1

        return nbIsles

    def getIsle(self, cell, vus = [], isle = True):
        if (cell in vus):
            return

        vus.append(cell)

        for v in cell.voisins:
            if isle:
                if v.isIsle():
                    self.getIsle(v, vus, isle)

            else:
                if v.isLake():
                    self.getIsle(v, vus, isle)  

    def keyboardEvents(self, event):
        touche = event.keysym
        if touche == "Escape":
            self.quit()

    def quit(self, event = None):
        self.fen.destroy()

    def clean(self):
        self.can.delete("all")


if __name__ == "__main__":
    g = Main()
