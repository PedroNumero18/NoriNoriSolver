# NoriNoriSolver

## Description
NoriNoriSolver is a Python project designed to generate and solve NoriNori grids. The program generates random grids, converts them into DIMACS format, and uses a SAT solver to find a solution. **Please note that this project is still under development and may not be ever fully functional.**

## Project Structure

- **main.py**: The main entry point of the program.
- **DIMACS/**: Contains the generated DIMACS files, including CNF clauses.
- **doc/**: Contains documentation related to the project.
- **Module/**: Contains the Python modules required for the project:
  - `DimacsGen.py`: Generates DIMACS files from NoriNori grids.
  - `DPLL.py`: Implements a SAT solver based on the DPLL algorithm.
  - `NoriGrid.py`: Generates and manipulates NoriNori grids.
  - `regles.py`: Defines the specific rules for the NoriNori game.
  - `SatSolver.py`: Interface for solving DIMACS files.

## Prerequisites

- Python 3.11 or higher
- Standard Python modules: `math`, `random`

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone <REPOSITORY_URL>
   ```
2. Ensure Python 3.11 or higher is installed.

## Usage

1. Run the `main.py` file:
   ```bash
   python main.py
   ```
   or
   ```bash
   python3 main.py
   ```
2. Follow the terminal instructions to:
   - Generate a random NoriNori grid.
   - Display the generated DIMACS clauses.
   - Solve the grid using the SAT solver.

## Features

- Random generation of NoriNori grids.
- Conversion of grids into DIMACS format.
- Solving grids using a SAT solver.

## Authors

This project was created as part of the INF402 course.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
