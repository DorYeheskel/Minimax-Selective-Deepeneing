#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
This file has the main loop of the game.
The function "run_game()" is the main function of this file,
which call the other functions such as getaction functions.

"""

import chess
import chess.pgn
import utils
import algorithms
import datetime
from utils import print_info, log
from time import time


def get_move_from_user(board: chess.Board, depth=3, player_name='', algo='', is_filter=False, filter_args=None) -> (chess.Move, int):
    utils.print_board(board)
    start_time = time()
    while True:
        move_str = str(input("Enter move: "))
        move: chess.Move = chess.Move.from_uci(move_str)
        if move not in board.legal_moves:
            print('-E-', 'Illegal move. Try again ...')
            continue
        end_time = time()
        time_of_turn = end_time - start_time
        delta = datetime.timedelta(seconds=time_of_turn)
        log(player_name + ': ' + str(move) + ' (Time:' + str(delta))
        return move, time_of_turn


def get_move_from_agent(board: chess.Board, depth=3, player_name='', algo='', is_filter=False, filter_args=None) -> (
        chess.Move, int):
    start_time = time()
    move = algorithms.get_action(state=board, deciding_agent=board.turn, algo=algo, depth=depth, is_filter=is_filter,
                                 filter_args=filter_args)  # <-- here is the main function and algorithem
    end_time = time()
    time_of_turn = end_time - start_time
    delta = datetime.timedelta(seconds=time_of_turn)
    print_info(player_name + ': ' + str(move) + '\t\t| Move time:' + str(delta) + '')
    return chess.Move.from_uci(str(move)), time_of_turn


def run_game(board: chess.Board, player1, player2, max_depth1: int, max_depth2: int, max_moves: int, max_time: int,
             is_filter1: bool, is_filter2: bool, keep_rate: float, teta: float, gama: float):
    filter_args = {'keep_rate': keep_rate, 'teta': teta, 'gama': gama}
    utils.print_game_settings(player1, player2, max_depth1, max_depth2, max_moves, max_time, is_filter1, is_filter2,
                              **filter_args)

    # Define move function for each player:
    algorithm_map = {'Player 1': player1,
                     'Player 2': player2}
    move_function = {'Player 1': get_move_from_agent if player1 != 'human' else get_move_from_user,
                     'Player 2': get_move_from_agent if player2 != 'human' else get_move_from_user}
    depths = {'Player 1': max_depth1,
              'Player 2': max_depth2}
    is_filters = {'Player 1': is_filter1,
                  'Player 2': is_filter2}

    # Define clock for each player:
    times = {'Player 1': max_time, 'Player 2': max_time}  # if one of them is negative, player lost
    moves = {'Player 1': 0, 'Player 2': 0}

    print_info("------------------- GAME START -------------------")
    winner_player = 'DRAW'
    curr_move_idx = 0
    while not board.is_game_over():
        # Choose current player:
        curr_player = 'Player 1' if curr_move_idx % 2 == 0 else 'Player 2'
        curr_color = board.turn
        moves[curr_player] += 1

        # Get move and time it took:
        get_move = move_function[curr_player]
        move, time_of_turn = get_move(board, player_name=curr_player, algo=algorithm_map[curr_player],
                                      depth=depths[curr_player], is_filter=is_filters[curr_player],
                                      filter_args=filter_args)

        # Update time and check if the player time is over:
        times[curr_player] -= time_of_turn
        if times[curr_player] < 0:
            winner_player = 'Player 2' if curr_move_idx % 2 == 0 else 'Player 1'
            print_info(curr_player + ' ran out of time ... Lost the game')
            break

        # Check if the move will do a check:
        if board.gives_check(move):
            print_info(curr_player + ' did a check')

        # Do the move:
        board.push(move)

        # Check if it made checkmate:
        if board.is_checkmate():
            winner_player = curr_player
            break

        # Update total moves:
        curr_move_idx += 1
        if curr_move_idx == max_moves:
            print_info('Too many moves ...')
            break

        # Check for 3 repetitions:
        if board.is_repetition():
            print_info('3 repetitions detected ...')
            break

    print_info('Winner: ' + winner_player)
    print_info("------------------- GAME END -------------------")

    # Print time details:
    utils.print_time_details(times, max_time)

    # EXPERIMENTS PRINTS:
    # ---------------------------------------------------------------------------
    # Print Average time for move: (for experiments)
    avg_1 = utils.get_time_usage(times['Player 1'], max_time) / moves['Player 1']
    if moves['Player 2'] != 0:
        avg_2 = utils.get_time_usage(times['Player 2'], max_time) / moves['Player 2']
    else:
        avg_2 = 0

    print('-I- AVG_PLAYER_1: ' + str(avg_1))
    print('-I- AVG_PLAYER_2: ' + str(avg_2))

    # Print to stdout Winner: (for experiments)
    print('-I- WINNER: ' + winner_player)

