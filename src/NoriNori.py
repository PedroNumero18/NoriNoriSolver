import random
class NoriNori:
    def __init__(self, size: (int)) -> None:
        self.grid = [[(int,int)]]
        self.size = size
    
    def initGrid(self) -> None:
        for i in range(self.size):
            for j in range(self.size): 
                self.grid.append([(i, j)])
        i = self.grid
    def isNeighbor(self,couple) -> bool:
        i = self.grid[[]].index(couple)
        
    def printGrid(self) -> None:
        for i in self.grid:
            if i[0][1] ==0:
                print("\n")
            print(*i, end="")
        print("\n")

    



if __name__ =="__main__":
    Nori = NoriNori(6)
    Nori.initGrid()
    Nori.printGrid()