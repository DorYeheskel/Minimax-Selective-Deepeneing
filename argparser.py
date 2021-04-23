#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
File for parsing the arguments for main.py.
To see the full usage of these arguments, run:
> python main.py --help

"""

import argparse
from chess import STARTING_FEN


def parsing_arguments():
    parser = argparse.ArgumentParser(prog='Project_AI_Chess_Dor_Doron', description='Project in AI chess, created by Dor Y and Doron G')
    algo_list = ['minimax', 'alpha_beta', 'human', 'random']
    args_with_param = [
        (('--fen', '-fen'),
         {'help': 'Customize & copy FEN value (with "") from: https://lichess.org/editor', 'required': False,
          'type': str, 'default': STARTING_FEN}),
        (('--player1', '-player1'),
         {'help': 'minimax/alpha_beta/human/random (default: alpha_beta)',
          'required': False,
          'choices': algo_list,
          'type': str, 'default': 'alpha_beta'}),
        (('--player2', '-player2'),
         {'help': 'minimax/alpha_beta/human/random (default: alpha_beta)',
          'required': False,
          'choices': algo_list,
          'type': str, 'default': 'alpha_beta'}),
        (('--max_moves', '-max_moves'), {'help': 'Total moves of the game (default: 100)', 'required': False, 'type': int, 'default': 100}),
        (('--max_time', '-max_time'),
         {'help': 'Total game time in seconds (default: 120 sec (60 sec for each player))', 'required': False,
          'type': int, 'default': 2 * 60}),
        (('--max_depth1', '-max_depth1'),
         {'help': 'Player 1 max depth of min_max algorithem (default: 3)', 'required': False,
          'choices': [1, 2, 3, 4, 5, 6], 'type': int, 'default': 3}),
        (('--max_depth2', '-max_depth2'),
         {'help': 'Player 2 max depth of min_max algorithem (default: 3)', 'required': False,
          'choices': [1, 2, 3, 4, 5, 6], 'type': int, 'default': 3}),
        (('--keep_rate', '-keep_rate'),
         {'help': 'Keep rate (default: 0.75)', 'required': False,
          'type': float, 'default': 0.75}),
        (('--teta', '-teta'),
         {'help': 'Weight of the moves improvement in the heuristic, during moves filter (default: 0.6)',
          'required': False,
          'type': float, 'default': 0.6}),
        (('--gama', '-gama'),
         {'help': 'Weight of the tools in the heuristic, during moves filter (default: 0.4)', 'required': False,
          'type': float, 'default': 0.4}),
        (('--log_f_name', '-log_f_name'),
         {'help': 'log file (path)', 'required': False, 'type': str, 'default': './tmp/game.log'}),
        (('--pgn_f_name', '-pgn_f_name'),
         {'help': 'pgn file (path)', 'required': False, 'type': str, 'default': './tmp/game.pgn'}),
        (('--out_f_name', '-out_f_name'),
         {'help': 'Output file name (default: stdout)', 'required': False, 'type': str})
    ]
    args_bool = [(('--open_lichess', '-open_lichess'),
                  {'help': 'Open lichess site to paste the pgn in the end', 'action': 'store_true'}),
                 (('--filter1', '-filter1'),
                  {'help': 'Use filter algorithem during minimax/alpha_beta/random for player 1',
                   'action': 'store_true'}),
                 (('--filter2', '-filter2'),
                  {'help': 'Use filter algorithem during minimax/alpha_beta/random for player 2',
                   'action': 'store_true'})]
    for arg in (args_with_param + args_bool):
        parser.add_argument(*arg[0], **arg[1])
    return parser.parse_args()
