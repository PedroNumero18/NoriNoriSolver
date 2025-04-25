from src.NoriNori import *

def main():
    N = int(input("entrer la taille du terrain \n"))
    Nori = NoriNori(N)
    Nori.initGrid()
    Nori.grid[0][0][1]
    Nori.printGrid()
    print(Nori.isNeighbor((1,3), (1,2)))
    FileName = str(input("what is the file name or storage \n"))
    Nori.writeGrid(FileName)


if __name__ =="__main__":
    main()