Usage
=====

Change the `command` in `config.yml` to use your own Go program command (Only leela zero supported now), you can also use `--command` option to override the config.

`./run.py` will run all tests

`./run.py -h` for help

Example output:

```
Boods-MacBook-Pro:go-test Bood$ ./run.py
Command: /Users/Bood/mypro/leela-zero/bin/leelaz -d -t 1 -p 1600 --noponder -w /Users/Bood/mypro/leela-zero/bin/af9
ladder1.sgf
[FAIL]  C17 ->     254 (V: 39.95%) (N:  8.68%) PV: C17 B15 E18 D17 D18 B17 B18 C16 C18 F18 A17 B16 P7 O7
ladder2.sgf
[PASS]   E1 ->     893 (V: 40.28%) (N: 42.68%) PV: E1 G4 E9 E10 F10 E11 D9 C12 D14 F9 C9
ladder3.sgf
[FAIL]  P11 ->     708 (V: 57.36%) (N:  0.17%) PV: P11 N11 O12 O13 N12 M12 N13 N14 M13 L13 M14 M15 L14 K14 L15 L16 K15
ladder4.sgf
[PASS]  C16 ->     660 (V: 27.50%) (N:  0.09%) PV: C16 P6 D17 P2 Q2 F3 P3 O3
ladder5.sgf
[PASS]   O7 ->     792 (V: 45.98%) (N: 23.54%) PV: O7 J6 P6 O5 C11 C9 E12 E13 F13
lifedeath1.sgf
[FAIL]   M9 ->    1318 (V: 97.09%) (N: 61.30%) PV: M9 S18 T18 S19 R19 S16 T19 S15 S14 R14 T15 Q16 T16 Q15
longdragon1.sgf
[FAIL]   D8 ->     524 (V: 96.66%) (N:  6.78%) PV: D8 D9 D7 C9 E9 D10 F9 G9
longdragon2.sgf
[FAIL]   N5 ->     754 (V: 94.61%) (N:  0.40%) PV: N5 L5 O6 T2 L17 J5 K18 K16
```


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
