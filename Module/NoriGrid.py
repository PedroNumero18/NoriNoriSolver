import random
from typing import List, Dict, Tuple, Optional

class NoriGrid:
    def __init__(self, width: int, height: int, num_regions: Optional[int] = None) -> None:
        self.grid: list[list[int]] = []
        self.height = height
        self.width = width
        # Dictionnaire qui stocke les cellules de chaque région
        # Clé: identifiant de région, Valeur: liste de tuples (row, col)
        self.regions: Dict[int, List[Tuple[int, int]]] = {}
        
        if (self.height <= 0 or self.width <= 0 or self.height * self.width != self.height**2):
            print("error: invalid grid size")
            
            
        # Initialiser la grille avec des zéros (cellules non assignées)
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(0)
            self.grid.append(row)
        
        # Si on veut une grille simple avec des identifiants séquentiels
        if num_regions is None and self.height == self.width:
            count = 1
            for i in range(self.height):
                for j in range(self.width):
                    self.grid[i][j] = count
                    # Ajouter cette cellule à son propre groupe (chaque cellule est une région)
                    self.regions[count] = [(i, j)]
                    count += 1
        # Sinon, générer des régions aléatoires
        else:
            if num_regions is None:
                # Par défaut, créer environ n²/4 régions
                num_regions = max(1, (width * height) // 4)
            
            self.generate_random_regions(num_regions)
        
        # Vérifier que toutes les régions ont au moins 2 cellules
        self._validate_regions()
    
    def _validate_regions(self) -> None:
        """Vérifie que toutes les régions ont au moins 2 cellules."""
        invalid_regions = []
        for region_id, cells in self.regions.items():
            if len(cells) < 2:
                invalid_regions.append(region_id)
        
        if invalid_regions:
            # Fusionner les régions invalides avec leurs voisines
            for region_id in invalid_regions:
                cells = self.regions[region_id]
                # Trouver une région voisine
                neighbor_region = None
                for r, c in cells:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < self.height and 0 <= nc < self.width and 
                            self.grid[nr][nc] != region_id):
                            neighbor_region = self.grid[nr][nc]
                            break
                    if neighbor_region:
                        break
                
                # Si aucune région voisine, prendre n'importe quelle autre région
                if not neighbor_region:
                    for other_id in self.regions.keys():
                        if other_id != region_id:
                            neighbor_region = other_id
                            break
                
                # Fusionner avec la région voisine
                if neighbor_region:
                    for r, c in cells:
                        self.grid[r][c] = neighbor_region
                        self.regions[neighbor_region].append((r, c))
                    del self.regions[region_id]
    
    def generate_random_regions(self, num_regions: int) -> None:
        """
        Génère des régions aléatoires dans la grille.
        
        Args:
            num_regions: Le nombre souhaité de régions
        """
        # S'assurer que le nombre de régions est sensé
        total_cells = self.width * self.height
        max_regions = total_cells // 2  # Besoin d'au moins 2 cellules par région
        num_regions = min(num_regions, max_regions)
        
        # Initialiser le dictionnaire des régions
        self.regions = {}
        
        # Garder trace des cellules déjà assignées
        unassigned_cells = [(i, j) for i in range(self.height) for j in range(self.width)]
        random.shuffle(unassigned_cells)
        
        for region_id in range(1, num_regions + 1):
            # Choisir une taille pour cette région (entre 2 et 6 cellules)
            region_size = random.randint(2, min(6, len(unassigned_cells)))
            
            # Si pas assez de cellules restantes, terminer
            if len(unassigned_cells) < region_size:
                break
                
            # Initialiser la liste des cellules de cette région
            self.regions[region_id] = []
                
            # Sélectionner la première cellule de cette région
            seed_cell = unassigned_cells.pop()
            current_region = [seed_cell]
            self.grid[seed_cell[0]][seed_cell[1]] = region_id
            self.regions[region_id].append(seed_cell)
            
            # Grandir la région à partir de la cellule de départ
            for _ in range(region_size - 1):
                # Trouver des cellules adjacentes non assignées à une région existante
                candidates = []
                for cell in current_region:
                    r, c = cell
                    neighbors = []
                    # Vérifier les 4 directions
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < self.height and 0 <= nc < self.width and 
                            (nr, nc) in unassigned_cells):
                            neighbors.append((nr, nc))
                    candidates.extend(neighbors)
                
                # S'il n'y a plus de cellules adjacentes disponibles, chercher n'importe quelle cellule
                if not candidates:
                    # Si on ne peut pas grandir la région davantage, on arrête
                    break
                
                # Sélectionner une cellule adjacente au hasard
                next_cell = random.choice(candidates)
                unassigned_cells.remove(next_cell)
                current_region.append(next_cell)
                self.grid[next_cell[0]][next_cell[1]] = region_id
                self.regions[region_id].append(next_cell)
        
        # S'il reste des cellules non assignées, les ajouter à des régions existantes
        while unassigned_cells:
            cell = unassigned_cells.pop()
            r, c = cell
            
            # Chercher des régions adjacentes
            adjacent_regions = set()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.height and 0 <= nc < self.width and 
                    self.grid[nr][nc] > 0):
                    adjacent_regions.add(self.grid[nr][nc])
            
            # Si il y a des régions adjacentes, choisir l'une d'entre elles
            if adjacent_regions:
                chosen_region = random.choice(list(adjacent_regions))
            else:
                # Sinon, choisir n'importe quelle région existante
                existing_regions = list(self.regions.keys())
                chosen_region = random.choice(existing_regions)
                
            # Ajouter cette cellule à la région choisie
            self.grid[r][c] = chosen_region
            self.regions[chosen_region].append((r, c))
   
    def printGrid(self) -> None:
        """Affiche la grille et des informations sur les régions."""
        for i in range(self.height):
            # Affiche chaque élément avec alignement fixe
            print(f"{self.grid[i]}")
        
        # Afficher des statistiques sur les régions
        print("\nInformations sur les régions:")
        print(f"Nombre total de régions: {len(self.regions)}")
        for region_id, cells in self.regions.items():
            print(f"Région {region_id}: {len(cells)} cellules")
    
    def get_region_cells(self, region_id: int) -> List[Tuple[int, int]]:
        """
        Récupère toutes les cellules d'une région spécifique.
        
        Args:
            region_id: L'identifiant de la région
            
        Returns:
            Une liste de coordonnées (row, col) des cellules dans cette région
        """
        if region_id in self.regions:
            return self.regions[region_id]
        return []
    
    def get_cell_region(self, row: int, col: int) -> int:
        """
        Récupère l'identifiant de la région à laquelle appartient une cellule.
        
        Args:
            row: La ligne de la cellule
            col: La colonne de la cellule
            
        Returns:
            L'identifiant de la région, ou 0 si hors limites
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return 0

if __name__ == "__main__":
    w = int(input("entrer la longueur du terrain \n"))
    h = int(input("entrer la largeur du terrain \n"))
    Nori = NoriGrid(w, h, 9)  
    Nori.printGrid()
    Filename: str =input("What is the file name: \n")
    Nori.writeGrid(Filename)
