## Minimax selective deepening:
## What is it:
A variant of the minimax algorithem, which allowed the agent to increase the depth of the search (in comparison to normal minimax with the same time resource), with the tradeoff of loosing precent of the states in the minimax tree search, with a "smart" filtering (heuristic).
<br />
<br />
The pasudo-code for rb-minimax / rb-alphabeta algorithems can be found in the etc directory.
<br />
<br />
The demonstration of the variant done in **Chess**.
<br />
## In the repository:
* Python implementations:
    * Resource bound Minimax/Alphabeta algorithms.
    * The Minimax selective deepening variant.
    * Chess game.
    * Chess heuristics: 
        *  Heuristic to evaluate Chess state (the classic chess heuristic)
        *  Heuristic to evaluate the potential of Chess state (special for the variant)
* Experiments:
    * Parallel bash scripts to run experiments of time and agent's quality.
    * Script to plot the graphs (using matplotlib). 
* Paper (Hebrew).

## How to install:
- git clone https://github.com/DorYeheskel/Minimax-Selective-Deepeneing.git
- pip install -r requirements.txt
- python main.py \<optional arguments\>

## Usage example:
To see all the flags options: <br />
*\> main.py --help*
<br />
Running: <br />
*\> main.py \<optional arguments\>*
<br />
## Example 1: Play the game
Running a Chess game which player_1 and player_2 are both alphabeta agents:<br />
![chess](https://user-images.githubusercontent.com/38854355/114739432-89846880-9d51-11eb-8f69-95b47cb285b6.gif)
**Notes:**
* There are a lot of parameters and combinations for each player (e.g the max depth of the tree for each player, precent of filtering, etc.). To see all the options, and the defaults, do "--help". 
* There is also an option to play as human (using keyboard (stdin)).
* In the end of the game, the full game will be copy to your clipboard as PGN Chess data (and PGN file will also creat automatically), and with option "--open_lichess", the Chess website will open and all you have to do is to paste, as you can see below. 


## Example 2: See the game
After the game ended, you can open lichess website (or automatically open with "--open_lichess") and you can just paste the game:<br />

![chess_lichess](https://user-images.githubusercontent.com/38854355/114857158-a0c66300-9df0-11eb-9ca0-66e6cfae875f.gif)



