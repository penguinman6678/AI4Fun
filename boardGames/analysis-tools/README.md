### Run to generate a training data that has three columns
- column 1 -- x
- column 2 -- y in board display format
- column 3 -- y in a training label format as predicting a next movement

#### Commands to run
- game_output_1k_sample.log
   - is the file from the simulations -- e.g. MCTS vs MCTS
   - is 1k sampled from game_output.log from directory boardGames
```
$>python3 game_data_load_parse_v1.py game_output_1k_sample.log
```
