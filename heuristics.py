#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
This file contain the 2 evaluation functions,
each of them evaluation the given state.

1) evaluation      : Basic heuristic.
2) evaluation_move : Heuristic in order to sort the moves.

"""

import numpy as np
import chess
import utils
from math import sqrt


# Global map:
piece_value_map = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 0
}

piece_loc_map = {
    chess.PAWN: utils.WHITE_PAWN_LOC_VAL,
    chess.KNIGHT: utils.WHITE_KNIGHT_LOC_VAL,
    chess.BISHOP: utils.WHITE_BISHOP_LOC_VAL,
    chess.ROOK: utils.WHITE_ROOK_LOC_VAL,
    chess.QUEEN: utils.WHITE_QUEEN_LOC_VAL,
    chess.KING: utils.WHITE_KING_LOC_VAL
}


# -------------------------------------------------------------------------------------------------------------------
# Evaluation function:

def evaluation(board: chess.Board, deciding_agent):
    """
    Basic heuristic.

    :param board: The current state of the game The current state of the game
    :param deciding_agent: The identity of the "good" agent.
    :return: Heuristic value for the state
    """
    # Define 1 for myself and -1 for rival:
    eval_num = 1 if board.turn != deciding_agent else -1

    # Check for corner cases:
    if board.is_checkmate():
        return 10000000000 * eval_num
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Calculate board value:
    material = 0
    material += eval_board(board) * eval_num

    # Check if check is possible and give small reward for that:
    if board.is_check():
        material += 80 * eval_num

    return material


# -------------------------------------------------------------------------------------------------------------------
# Evaluation function for filter:

def evaluation_move(board: chess.Board, move: chess.Move, total_moves, teta: float, gama: float) -> float:
    """
    Heuristic in order to sort the moves.

    :param board: The current state of the game
    :param move: The current move
    :param teta: Weight of the moves improvement in the heuristic
    :param gama: Weight of the tools in the heuristic
    :return: Heuristic value for the state
    """
    # Check for corner cases:
    if is_move_create_checkmate(board, move):
        return np.inf
    if is_move_create_3_repetition(board, move):
        return -np.inf

    # Get value of the current tool:
    piece: chess.Piece = board.piece_at(move.from_square)
    piece_value = piece_value_map[piece.piece_type] / 10

    # Estimate total moves that added by this future move:
    moves_improve_value = get_move_improvement(board, move, piece, total_moves)

    # Check binary situations:
    if board.is_attacked_by(color=not board.turn, square=move.from_square): return 1000000
    if board.is_capture(move): return 1000000
    if board.is_attacked_by(color=not board.turn, square=move.to_square): return -100000

    # Calculate the value based on teta and gama:
    move_value = moves_improve_value * teta + piece_value * gama

    return move_value


# -------------------------------------------------------------------------------------------------------------------
# Utils functions:

def get_move_improvement(board: chess.Board, move: chess.Move, piece: chess.Piece, total_moves: int):
    """
    Get move improvement: The number of the moves that the current move created,
                        in comparision to the state before.

    :param total_moves:
    :param board: The current state of the game
    :param move: The current move
    :return: The move improvement value
    """
    tmp_board = board.copy()
    tmp_board.remove_piece_at(move.from_square)
    tmp_board.set_piece_at(move.to_square, piece=piece)
    delta = tmp_board.legal_moves.count() - total_moves
    return delta


def is_move_create_checkmate(board: chess.Board, move: chess.Move) -> bool:
    """

    :param board: The current state of the game
    :param move: The current move
    :return: True if move that create checkmate detected, else False
    """
    board.push(move)
    is_checkmate = True if board.legal_moves.count() == 0 else False
    board.pop()
    return is_checkmate


def is_move_create_3_repetition(board: chess.Board, move: chess.Move) -> bool:
    """
    :param board: The current state of the game
    :param move: The current move
    :return: True if 3 repetitions detected, else False
    """
    board.push(move)
    is_repet = True if board.is_repetition() else False
    board.pop()
    return is_repet


def eval_board(board: chess.Board):
    """
    Evaluate the board by the pieces values.

    :param board: The current state of the game
    :return: board evaluation, based on the pieces
    """
    whites = 0
    black = 0
    for sqare_idx in chess.SQUARES:
        piece = board.piece_at(sqare_idx)
        if piece is None:
            continue
        if piece.color == chess.WHITE:
            whites += piece_value_map[piece.piece_type] + get_piece_location_value(piece.piece_type, piece.color, sqare_idx)
        else:
            black += piece_value_map[piece.piece_type] + get_piece_location_value(piece.piece_type, piece.color, sqare_idx)
    return abs(whites - black)


def get_piece_location_value(piece: chess.PieceType, color: chess.Color, sqare_idx: int):
    row, column = square_to_row_and_col(color, sqare_idx)
    piece_map_val = piece_loc_map[piece]
    if color == chess.BLACK:
        piece_map_val = piece_map_val[::-1]
    piece_location_value = piece_map_val[row][column]
    return piece_location_value


def square_to_row_and_col(color: chess.Color, sqare_idx: int) -> tuple:
    column, row = sqare_idx % 8, 0
    if color == chess.WHITE:
        row = 7-(sqare_idx//8)
    else:
        row = sqare_idx//8
    return row, column


def euclidean_distance_board(a: chess.Square, b: chess.Square) -> float:
    """
    Helper function to calculate the distance between to squares.

    :param a: square 1
    :param b: square 2
    :return: distance
    """
    return sqrt((chess.square_file(a) - chess.square_file(b)) ** 2 + (chess.square_rank(a) - chess.square_rank(b)) ** 2)

