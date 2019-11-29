# For Tic-Tae-Toe
### What is about Tic-Tae-Toe
1. Definition
2. Playing Rules
### Why this game is selected for demonstration here-- especially w.r.t. A.I.
1. Computational Challenges
2. Winning strategy by Human, and how this can be translated for an AI algorithm
3. How to extend this idea to other games like [Go](https://deepmind.com/research/case-studies/alphago-the-story-so-far)

## Game.py --  the main module to run a game
```sh
$>python3 game.py
```
   - this will save output (a json object) to "./game_output.log" 
#### Update
|Date | Summary|
| ------ | ------ |
|Nov 28 2019 | game.py is now based on human and an agent. The agent is now using the policy of MCTS, which also needs more improvement. This can be considered as V0.5 of MCTS policy  |
|Oct 31 2019 | game.py is based on two agent playing which will dump outputs of history of movements as well as drawing steps/movements in a canvas using Turtle  |
|Oct 29 2019 | game.py is based on two agent playing which will dump outputs of history of movements  |

###
#### Things to do
1. Need to add a functionality to allow a user to select an option for 1) computer (agent) vs computer (agent)
2. Update the function from board.py to tell if a component is connected for a winning -- much smarter way
3. Add an evaluation function to find an optimal movement given a state of the board
4. Need to improve MCTS policies using smarter choices -- You will see the drawbacks of MCTS. :)

#### Things done
1. user vs. computer, where computer is based on MCTS -- Nov 28 2019