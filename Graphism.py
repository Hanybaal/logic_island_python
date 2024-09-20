from random import randint

class Graphism():
    def __init__(self, fen):
        self.main = fen
        self.fen = fen.fen
        self.can = fen.can
        self.tx = fen.size1 - 6
        self.ty = fen.size2 - 6
        self.grid = fen.grid

        nx, ny = self.grid.getSizeX(), self.grid.getSizeY()
        self.pax, self.pay = self.ty/nx, self.ty/ny
        
        self.graphicalGrid = []
        self.graphicalSizes = []

    def getGraphism(self):
        g = self.grid
        ox, oy = self.tx/2 - self.ty/2 + 2, 0 + 2
        nx, ny = self.grid.getSizeX(), self.grid.getSizeY()
        cfb = 50

        self.can.create_rectangle(ox - self.pay/10, oy - 10,
                                  ox + self.ty + self.pay/10, oy + self.ty + 10,
                                  outline = "black", fill = "aquamarine")
        
        for i in range(ny):
            self.graphicalGrid.append([])
            for j in range(nx):
                cell = self.grid.getCellule(i, j)
                case = self.can.create_polygon(
                        ox + j*self.pax, oy + i*self.pay,
                        ox + j*self.pax + self.pax/2, oy + i*self.pay + self.pay/cfb,
                        ox + (j + 1)*self.pax, oy + i*self.pay,
                        ox + (j + 1)*self.pax - self.pax/cfb, oy + i*self.pay + self.pay/2,
                        ox + (j + 1)*self.pax, oy + (i + 1)*self.pay,
                        ox + j*self.pax + self.pax/2, oy + (i + 1)*self.pay - self.pay/cfb,
                        ox + j*self.pax, oy + (i + 1)*self.pay,
                        ox + j*self.pax + self.pax/cfb, oy + i*self.pay + self.pay/2,
                        fill = self.getColor(cell),
                        outline = self.getColor(cell),
                        tags = "cell" + str(i) + str(j))

##                case = self.can.create_rectangle(
##                        ox + j*self.pax, oy + i*self.pay,
##                        ox + (j + 1)*self.pax, oy + (i + 1)*self.pay,
##                        fill = self.getColor(cell),
##                        outline = self.getColor(cell),
##                        tags = "cell" + str(i) + str(j))

                self.graphicalGrid[-1].append(case)
                self.can.tag_bind("cell" + str(i) + str(j), "<Button-1>", self.changeCellState)

    def genereSizes(self, aleaTerrain, size):
        ox, oy = self.tx/2 - self.ty/2 + 2, 0 + 2
        #aleaTerrain = isle[randint(0, s - 1)]

        gs = self.can.create_text(ox + aleaTerrain.getX()*self.pax + self.pax/2,
                                  oy + aleaTerrain.getY()*self.pay + self.pay/2,
                                  text = str(size),
                                  font = ('Georgia 15 bold'))

    def getColor(self, cell):
        if (cell.isLake()):
            return "aquamarine"

        if (cell.isIsle()):
            return "goldenrod1"

    def changeCellState(self, event):
        x, y = event.x, event.y
        ox, oy = self.tx/2 - self.ty/2 + 2, 0 + 2
        ix = int((event.x - ox)*self.grid.getSizeX() / self.ty)
        iy = int((event.y - oy)*self.grid.getSizeY() / self.ty)
        cell = self.grid.getCellule(iy, ix)
        case = self.graphicalGrid[iy][ix]
        
        cell.changeState()
        self.can.itemconfigure(case, fill = self.getColor(cell))
        self.can.itemconfigure(case, outline = self.getColor(cell))

        self.main.verifications()
