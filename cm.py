import pyautogui
import win32api
import random
from typing import List
from time import sleep


class Cell():
    def __init__(self, state, valor=0):
        self.state = state
        self.mostrando = False
        self.valor = valor
    

class Grid():
    def __init__(self, size):
        self.size = size
        self.p1 = 0 # ES
        self.p2 = 0 # DS
        self.p3 = 0 # EI
        self.p4 = 0 # DI
        self.grid: List[List[Cell]] = self.generateGrid()
        self.bombas = (int((size*size)/100*15), 0)

    def setGrid(self, x1, y1, x2, y2):
        self.p1 = (x1, y1) # ES
        self.p2 = (x2, y1) # DS
        self.p3 = (x1, y2) # EI
        self.p4 = (x2, y2) # DI

    def generateGrid(self):
        aux = []

        retorno: List[List[Cell]] = []
        tam = self.size*self.size
        num_bombas = int(tam/100*15)

        for _ in range(num_bombas):
            aux.append(Cell(1,"X"))
        while len(aux) < tam:
            aux.append(Cell(0))
        random.shuffle(aux)
        for i in range(0, len(aux), self.size):
            retorno.append(aux[i:i + self.size])

        for indexi, i in enumerate(retorno):
            for indexj, j in enumerate(i):
                try:
                    if indexi > 0 and indexj > 0 and retorno[indexi-1][indexj-1].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi > 0 and indexj >= 0 and retorno[indexi-1][indexj].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi > 0 and indexj >= 0 and retorno[indexi-1][indexj+1].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi >= 0 and indexj > 0 and retorno[indexi][indexj-1].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi >= 0 and indexj >= 0 and retorno[indexi][indexj+1].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi >= 0 and indexj > 0 and retorno[indexi+1][indexj-1].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi >= 0 and indexj >= 0 and retorno[indexi+1][indexj].state:
                        j.valor += 1
                except:
                    pass
                try:
                    if indexi >= 0 and indexj >= 0 and retorno[indexi+1][indexj+1].state:
                        j.valor += 1
                except:
                    pass

        return retorno

def genGrid():
    size = int(input("Digite o tamanho do grid X:X - "))
    return Grid(size)

def getPosGrid(grid: Grid):
    while True:
        if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
            x1, y1 = pyautogui.position()
            break
    sleep(0.3)
    while True:
        if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
            x2, y2 = pyautogui.position()
            break
    sleep(0.3)
    grid.setGrid(x1,y1,x2,y2)


def drawGrid(grid: Grid):
    print("\033[H\033[J", end="")
    for linha in grid.grid:
        # print('|'.join(map(lambda obj: str(obj.valor), linha)))
        print(' '.join(map(lambda obj: (str(obj.valor) if obj.valor != 0 else " ") if obj.mostrando else u'\u25A2', linha)))
    print(f"Bombas restantes: {grid.bombas[0]}")
    print(f"Bombas marcadas: {grid.bombas[1]}")


def mouseRelativoCMD(grid: Grid):
    x1, y1 = grid.p1
    x2, y2 = grid.p4
    largura = x2-x1
    altura = y2-y1
    lar_celula = largura / grid.size
    alt_celula = altura / grid.size
    while True and any(cel.mostrando == False for row in grid.grid for cel in row):
        if win32api.GetKeyState(0x04)<0: #if middle mouse button is pressed
            x, y = pyautogui.position()
            sleep(0.1)
            relX = x - x1
            relY = y - y1
            celXNum = int(relX/lar_celula)
            celYNum = int(relY/alt_celula)
            try:
                celula = grid.grid[celYNum][celXNum]
                if celula.valor != u'\u25A9':
                    celula.valor = u'\u25A9'
                    celula.mostrando = True
                    grid.bombas = (grid.bombas[0] - 1, grid.bombas[1] + 1)
                    drawGrid(grid)
                    sleep(0.1)
            except IndexError:
                pass
        if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
            x, y = pyautogui.position()
            sleep(0.1)
            relX = x - x1
            relY = y - y1
            celXNum = int(relX/lar_celula)
            celYNum = int(relY/alt_celula)
            try:
                celula = grid.grid[celYNum][celXNum]
                celula.mostrando = True
                if celula.state:
                    print("\033[H\033[J", end="")
                    print("VOCÊ PERDEU!!")
                    exit()
                if celula.valor == 0:
                    drawZero(grid, celYNum, celXNum)
                drawGrid(grid)
                sleep(0.1)
            except IndexError:
                pass
    print("!!!!! VOCÊ GANHOU PARABENS !!!!!")
    exit()

def drawZero(grid: Grid, y, x):
    for numY in range(3):
        for numX in range(3):
            # if grid.grid[numY-1][numX-1].valor == 0 and grid.grid[numY-1][numX-1].mostrando != True:
            try:
                if grid.grid[y-(numY-1)][x-(numX-1)].valor >= 0 and grid.grid[y-(numY-1)][x-(numX-1)].mostrando == False:
                    grid.grid[y-(numY-1)][x-(numX-1)].mostrando = True
                    if grid.grid[y-(numY-1)][x-(numX-1)].valor == 0:
                        drawZero(grid, y-(numY-1), x-(numX-1))
            except:
                pass

grid = genGrid()
drawGrid(grid)
getPosGrid(grid)
mouseRelativoCMD(grid)
# try:
# except Exception as err:
#     print(err)