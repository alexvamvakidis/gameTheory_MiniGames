# Combinatorial Games AI (NIM & Notakto)

This repository contains the implementation of classic combinatorial games in Python. The project focuses on developing an artificial intelligence opponent capable of perfect-play, based strictly on game thery algorithms.

This project was developed as part of the undergraduate course "Algorithmic Game Theory" at the Computer Engineering and Informatics Department (CEID) of the University of Patras.

## Algorithmic Approach

The game AI implements the principles of Impartial Games, evaluating Winning and Losing positions using the following methods:
* **Modulo Arithmetic** for single-pile games.
* **Bouton's Theorem (Nim-sum / Bitwise XOR)** for calculating equilibrium in multi-pile games.
* **MEX (Minimum Excluded value) Rule** for evaluating complex states.
  
## Contents (Implemented Games)

1. **Game 1: Single-Pile NIM**
   * A subtraction game with a single pile. Supports Normal and Misere play conventions via Modulo calculation.
2. **Game 2: Multi-Pile NIM**
   * A subtraction game with 3 piles. The algorithm evaluates the XOR sum to select the optimal move.
3. **Game 3: Notakto 3x3**
   * A single-symbol Tic-Tac-Toe variation. Supports Normal and Misere play via recursive MEX calculation.
4. **Game 4: Notakto 4x4**
   * Expansion to a 4x4 board. 

## Requirements and Execution

* Language: Python 3.13
* Graphical Interface: `pygame` library

Dependency installation:
```bash
pip install pygame

Running the project:

From the project root run the main menu (recommended):
```bash
python3 main_menu.py
```