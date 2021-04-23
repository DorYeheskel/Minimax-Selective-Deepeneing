#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
The main file of the project.
From here the game start to run.

To get all params and usage:
> python main.py --help

"""

import chess
import chess.pgn
import utils
import argparser
import game
import sys
from utils import print_info


def main():
    # Params:
    parse = argparser.parsing_arguments()
    fen = parse.fen
    player1 = parse.player1
    player2 = parse.player2
    max_moves = parse.max_moves
    max_time = parse.max_time
    max_depth1 = parse.max_depth1
    max_depth2 = parse.max_depth2
    is_filter1 = parse.filter1
    is_filter2 = parse.filter2
    keep_rate = parse.keep_rate
    teta = parse.teta
    gama = parse.gama
    pgn_f_name = parse.pgn_f_name
    out_f_name = parse.out_f_name
    open_lichess = parse.open_lichess

    # Define output file & open log file:
    if out_f_name is not None:
        sys.stdout = open(out_f_name, 'a')
    utils.open_log_file(parse.log_f_name)

    # Start game:
    board = chess.Board(fen=fen)
    game.run_game(board=board, player1=player1, player2=player2, max_depth1=max_depth1, max_depth2=max_depth2,
                  max_moves=max_moves, max_time=max_time, is_filter1=is_filter1, is_filter2=is_filter2,
                  keep_rate=keep_rate, teta=teta,
                  gama=gama)

    # Create *.pgn of the game:
    utils.save_pgn_file(board, pgn_f_name=pgn_f_name, player1=player1, player2=player2)

    # Open lichess:
    if open_lichess:
        utils.open_lichess()

    # More:
    print_info('------------------- More info -------------------')
    print_info('PGN file copied to your clipboard.')
    print_info('To fully anaylise the game, paste it to: https://lichess.org/paste')
    print_info('To customize board, use [--fen] option and copy FEN value from: https://lichess.org/editor')

    if out_f_name is not None:
        sys.stdout.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('-E-', e)
