import random
class NoriNori:
    def __init__(self, size: (int)) -> None:
        self.grid = []
        self.region = []
        self.size = size
    
    def initGrid(self) -> None:
        for i in range(self.size):
            for j in range(self.size): 
                self.grid.append([(i, j)])

    def initRegion(self) -> None:
        print("attend Ahki")
    
    def isNeighbor(self,coupleCheck: tuple[int, int], coupleNeighbor: tuple[int, int]) -> bool:
        if ((coupleNeighbor[0] == coupleCheck[0]+1) ^ (coupleNeighbor[1] == coupleCheck[1]+1)) or ((coupleNeighbor[0] == coupleCheck[0]-1) ^ (coupleNeighbor[1] == coupleCheck[1]-1)):
            return True
        else:
            return False       
        
    def printGrid(self) -> None:
        for i in self.grid:
            if i[0][1] == 0:
                print("\n")
            print(*i, end="")
        print("\n")

    def writeGrid(self, FileName: str) -> None:
        Fgrid = open(FileName,"w")
        Fgrid.write(str(self.size))
        for i in self.grid:
            if i[0][1] == 0:
                Fgrid.write("/")
                Fgrid.write("\n########## \n")
            Fgrid.write(str(*i))
            Fgrid.write(" ")
        Fgrid.write("f")

if __name__ == "__main__":
    N = int(input("entrer la taille du terrain \n"))
    Nori = NoriNori(N)
    Nori.initGrid()
    Nori.printGrid()
    print(Nori.isNeighbor((1,3), (1,2)))
    FileName = input("where is the file")
    Nori.writeGrid(FileName)