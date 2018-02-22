Usage
=====

Change the `command` to use your own Go program command (Only leela zero supported now), you can also use `--command` option to override the config.

`./run.py` will run all tests

`./run.py -h` for help


Add tests
=========

1. Put your sgf file in `sgf` dir, e.g. `ladder6.sgf`

2. Add an entry in `tests` section, with following information:
   * `sgf` file name
   * `group` test group it belongs to
   * `move` who's turn it is now
   * test condition, one of the following (only one will be used):
     - `yes_move`: a list of moves it should choose, fail otherwise 
     - `no_move`: a list of moves it should NOT choose, fail if the choosed move is in the list
     - `max_win_rate`: upper threshold of win rate of value network, fail if the program thinks it's higher

3. Verify your added test with `./run.py --case test_name`
