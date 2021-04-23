#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
File consist of the algorithms the agent use.

"""

import chess
import numpy as np
from math import ceil
from utils import log
from heuristics import evaluation, evaluation_move
from random import shuffle


# -------------------------------------------------------------------------------------------------------------------
# Get action function:

def get_action(state: chess.Board, deciding_agent, algo, depth: int, is_filter: bool, filter_args: dict) -> chess.Move:
    kwargs = {'state' : state, 'deciding_agent' : deciding_agent, 'depth' : depth, 'decay' : 0.9, 'is_filter' : is_filter, 'filter_args' : filter_args}
    if algo == 'alpha_beta':
        return get_action_alpha_beta(**kwargs)
    if algo == 'minimax':
        return get_action_minimax(**kwargs)
    if algo == 'random':
        return get_random_action(**kwargs)


# -------------------------------------------------------------------------------------------------------------------
# RB-MiniMax

def rb_mini_max(state: chess.Board, deciding_agent, depth: int, decay=0.9, is_filter=False, filter_args=None):
    if state.is_game_over(): return evaluation(state, deciding_agent)
    if depth == 0: return evaluation(state, deciding_agent)
    agent_to_move = state.turn
    children = list(state.legal_moves)
    if is_filter is True:
        children = filter_children(state, children, **filter_args)
    shuffle(children)
    if agent_to_move == deciding_agent:
        cur_max = -np.inf
        for c in children:
            move = chess.Move.from_uci(str(c))
            state.push(move)
            v = rb_mini_max(state, deciding_agent, depth - 1, 0.9,  is_filter, filter_args) * decay
            state.pop()
            cur_max = max(v, cur_max)
        return cur_max
    else:
        cur_min = np.inf
        for c in children:
            move = chess.Move.from_uci(str(c))
            state.push(move)
            v = rb_mini_max(state, deciding_agent, depth - 1, 0.9,  is_filter, filter_args) * decay
            state.pop()
            cur_min = min(v, cur_min)
        return cur_min


def get_action_minimax(state: chess.Board, deciding_agent, depth=3, decay=0.9, is_filter=False, filter_args=None) -> chess.Move:
    log('-------- get action --------')
    children = list(state.legal_moves)
    if is_filter is True:
        children = filter_children(state, children, **filter_args)
    shuffle(children)
    cur_max = -np.inf
    best_move = np.random.choice(children)
    for c in children:
        move = chess.Move.from_uci(str(c))
        state.push(move)
        if state.is_repetition():
            state.pop()
            continue
        c_val = rb_mini_max(state, deciding_agent, depth - 1, 0.9, is_filter, filter_args)
        state.pop()
        log(str(move) + ' : ' + str(c_val))
        if c_val > cur_max:
            cur_max = c_val
            best_move = c
    log('Best: ' + str(best_move) + ' : ' + str(cur_max))
    return best_move


# -------------------------------------------------------------------------------------------------------------------
# RB-AlphaBeta:

def rb_alpha_beta(state: chess.Board, deciding_agent, depth: int, alpha, beta, decay=0.9, is_filter=False, filter_args=None):
    if state.is_game_over(): return evaluation(state, deciding_agent)
    if depth == 0: return evaluation(state, deciding_agent)
    agent_to_move = state.turn
    children = list(state.legal_moves)
    if is_filter is True:
        children = filter_children(state, children, **filter_args)
    shuffle(children)
    if agent_to_move == deciding_agent:
        cur_max = -np.inf
        for c in children:
            move = chess.Move.from_uci(str(c))
            state.push(move)
            v = rb_alpha_beta(state, deciding_agent, depth - 1, alpha, beta, 0.1, is_filter, filter_args) * decay
            state.pop()
            cur_max = max(v, cur_max)
            alpha = max(cur_max, alpha)
            if cur_max >= beta: return np.inf
        return cur_max
    else:
        cur_min = np.inf
        for c in children:
            move = chess.Move.from_uci(str(c))
            state.push(move)
            v = rb_alpha_beta(state, deciding_agent, depth - 1, alpha, beta, 0.1, is_filter, filter_args) * decay
            state.pop()
            cur_min = min(v, cur_min)
            beta = min(cur_min, beta)
            if cur_min <= alpha: return -np.inf
        return cur_min


def get_action_alpha_beta(state: chess.Board, deciding_agent, depth=3, decay=0.9, is_filter=False, filter_args=None) -> chess.Move:
    log('-------- get action --------')
    children = list(state.legal_moves)
    if is_filter is True:
        children = filter_children(state, children, **filter_args)
    shuffle(children)
    cur_max = -np.inf
    alpha, beta = -np.inf, np.inf
    best_move = np.random.choice(children)
    for c in children:
        move = chess.Move.from_uci(str(c))
        state.push(move)
        if state.is_repetition():
            state.pop()
            continue
        c_val = rb_alpha_beta(state, deciding_agent, depth - 1, alpha, beta, decay, is_filter, filter_args)
        state.pop()
        log(str(move) + ' : ' + str(c_val))
        if c_val > cur_max:
            alpha = c_val
            cur_max = c_val
            best_move = c
    log('Best: ' + str(best_move) + ' : ' + str(cur_max))
    return best_move


# -------------------------------------------------------------------------------------------------------------------
# Random:

def get_random_action(state: chess.Board, deciding_agent, depth=3, decay=0.9, is_filter=False, filter_args=None) -> chess.Move:
    children = list(state.legal_moves)
    if is_filter is True:
        children = filter_children_random(children, **filter_args)
    move = np.random.choice(children)
    return move


# -------------------------------------------------------------------------------------------------------------------
# Filter functions:

def filter_children(state: chess.Board, children: list, keep_rate=0.75, teta=0.6, gama=0.4) -> list:
    if keep_rate >= 1:
        return children
    children = sorted(children, key=lambda child: evaluation_move(state, child, len(children), teta, gama), reverse=True)
    idx_to_cut = ceil(len(children) * keep_rate)
    return children[:idx_to_cut]


def filter_children_random(children, keep_rate=0.75) -> list:
    if keep_rate >= 1:
        return children
    idx_to_cut = ceil(len(children) * keep_rate)
    return children[:idx_to_cut]
