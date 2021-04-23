#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
Utils file.
Contain helper functions for the rest of the script files.

"""

import logging
import os
import collections
import webbrowser as wb
import chess
import datetime
from time import sleep


def save_pgn_file(board: chess.Board, pgn_f_name: str, player1, player2):
    game = board_to_game(board)
    game.headers["Date"] = datetime.date.today()
    game.headers["White"] = player1
    game.headers["Black"] = player2
    game.headers["Result"] = board.result()
    print(game, file=open(pgn_f_name, "w"), end="\n\n")
    print_info('Save .pgn file at : ' + os.path.realpath(pgn_f_name))
    try:
        import pyperclip
        pyperclip.copy(str(game))
    except Exception as e:
        print_info('Module pyperclip doesnt exit. PGN file didnt copy to clipboard.')


def board_to_game(board: chess.Board):
    game = chess.pgn.Game()
    # Undo all moves.
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())
    game.setup(board)
    node = game
    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)
    return game


def open_lichess():
    url = 'https://lichess.org/paste'
    sleep(0.5)
    wb.open(url)


def print_board(board: chess.Board):
    uni_pieces = {'R': '♜',
                  'N': '♞',
                  'B': '♝',
                  'Q': '♛',
                  'K': '♚',
                  'P': '♟',
                  'r': '♖',
                  'n': '♘',
                  'b': '♗',
                  'q': '♕',
                  'k': '♔',
                  'p': '♙',
                  '.': '三'}
    res = str(board)
    for key, value in uni_pieces.items():
        res = res.replace(key, value)
    print(res)
    print('a一b一c一d一e一f一g一h')


def log(msg):
    # return None
    logging.info(msg)


def print_info(msg):
    # return None
    print('-I-', msg)
    logging.info(msg)


def print_error(msg):
    print('-E-', msg)
    logging.info(msg)


def get_time_usage(curr_time, max_time):
    return datetime.timedelta(seconds=max_time) - datetime.timedelta(seconds=curr_time)


def print_time_details(times, max_time):
    delta_1 = get_time_usage(times['Player 1'], max_time)
    delta_2 = get_time_usage(times['Player 2'], max_time)
    msg1 = 'Time used by Player 1: ' + str(delta_1) + ' (left: ' + str(
        datetime.timedelta(seconds=times['Player 1'])) + ')'
    msg2 = 'Time used by Player 2: ' + str(delta_2) + ' (left: ' + str(
        datetime.timedelta(seconds=times['Player 2'])) + ')'
    print_info(msg1)
    print_info(msg2)


def print_game_settings(player1, player2, max_depth1, max_depth2, max_moves, max_time, is_filter1, is_filter2,
                        keep_rate, teta, gama):
    print_info('------------------- INFO -------------------')
    print_info('Total game time             : ' + str(datetime.timedelta(seconds=max_time)))
    print_info('Total game for each player  : ' + str(datetime.timedelta(seconds=max_time / 2)))
    print_info('Player 1 (White)     : ' + player1)
    print_info('Player 2 (Black)     : ' + player2)
    print_info('Max moves            : ' + str(max_moves))
    print_info('Filter Player 1      : ' + str(is_filter1))
    print_info('Filter Player 2      : ' + str(is_filter2))
    print_info('Filter (keep_rate) : ' + str(keep_rate))
    print_info('Filter (teta)        : ' + str(teta))
    print_info('Filter (gama)        : ' + str(gama))
    print_info('Max depth Player 1   : ' + str(max_depth1))
    print_info('Max depth Player 2   : ' + str(max_depth2))


def open_log_file(f_path: str):
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    format_style = '[%(asctime)s] %(levelname)s %(message)s'
    date_format_style = '%a, %d %b %Y %H:%M:%S'
    logging.basicConfig(filename=f_path,
                        filemode='w',
                        format=format_style,
                        datefmt=date_format_style,
                        level=logging.DEBUG)
    print_info('-I- Log file path : ' + os.path.realpath(f_path))
    return f_path

# ------------------------------------------------------------------------------------------
# Chess locations matrix:

WHITE_PAWN_LOC_VAL = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

WHITE_KNIGHT_LOC_VAL = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

WHITE_BISHOP_LOC_VAL = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

WHITE_ROOK_LOC_VAL = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

WHITE_QUEEN_LOC_VAL = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

WHITE_KING_LOC_VAL = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

