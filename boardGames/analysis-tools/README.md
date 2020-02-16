### Run to generate a training data that has three columns
- column 1 -- x
- column 2 -- y in board display format
- column 3 -- y in a training label format as predicting a next movement

### mp4 file
- Based on a game log between two players, the mp4 file is to show the heat-map for a first move that lead to winning for a second player
- To view the videos of the simulations, check out [my blog at bugbytelab.com](https://bugbytelab.com/2020/02/03/example-of-moves-from-an-agent-to-win-a-game/).

#### Commands to run
- game_output_1k_sample.log
   - is the file from the simulations -- e.g. MCTS vs MCTS
   - is 1k sampled from game_output.log from directory boardGames
   - To produce a summary of the log
```
$>python3 game_data_load_parse.py game_output_1k_sample.log
```
  -  To produce a training data set from a log file
```
$>python3 game_data_load_parse.py game_output_1k_sample.log output_tag_for_training
```

- Deprecated below
```
$>python3 game_data_load_parse_v1.py game_output_1k_sample.log
```

