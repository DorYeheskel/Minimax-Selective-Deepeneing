#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd


def print_generic_graph(x_list, y_list, range_x, range_y, x_label, y_label, add_line=False, graph_name=None):
    if add_line is True:
        # Line and points:
        plt.plot(x_list, y_list, color='blue', linestyle='dashed', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=8)
    else:
        # Only points:
        for x, y in zip(x_list, y_list):
            plt.scatter(x, y, color='blue')

    # setting x and y axis range
    plt.xlim(range_x[0], range_x[1])
    plt.ylim(range_y[0], range_y[1])

    # naming the x axis
    plt.xlabel(x_label)

    # naming the y axis
    plt.ylabel(y_label)

    # giving a title to my graph
    if graph_name:
        plt.title(graph_name)

    # function to show the plot
    plt.show()


def print_time_grpah(f_name: str):
    df = pd.read_csv(f_name, sep=',', header=0)
    x = [2, 3, 4, 5, 6]
    colors = ['green', 'red', 'blue', 'yellow', 'brown', 'pink']
    for color, res in zip(colors, df.iterrows()):
        y = list(res[1])[1:]
        plt.plot(x, y, color=color, linestyle='dashed', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=8)

    # setting x and y axis range
    plt.ylim(0, 450)
    plt.xlim(0, 8)

    # naming the x axis
    plt.xlabel('Depth')
    # naming the y axis
    plt.ylabel('Avg time per move')

    # giving a title to my graph
    plt.title('Time experiments')

    # function to show the plot
    plt.show()


def print_params_graph(f_name: str):
    df = pd.read_csv(f_name, sep=',', header=0)
    teta = [0.05, 0.15, 0.3, 0.45, 0.55, 0.7, 0.85, 0.95]
    rank = df['rank']
    print_generic_graph(x_list=teta, y_list=rank, range_x=(0, 1), range_y=(0, 10), x_label='Teta', y_label='Rank', add_line=True, graph_name='Params experiments')


def print_rank_graph(f_name: str, depth: str):
    df = pd.read_csv(f_name, sep=',', header=0)
    keep_rate = [0.1, 0.2, 0.35, 0.4, 0.5, 0.6, 0.7]
    rank = df['rank']
    avg_time = df['avg_time_per_turn(sec)']
    for x, y, sec in zip(keep_rate, rank, avg_time):
        color = get_color_from_time(float(sec))
        plt.scatter(x, y, color=color)

    # setting x and y axis range
    plt.ylim(0, 10)
    plt.xlim(0, 1)

    # naming the x axis
    plt.xlabel('KeepRate')

    # naming the y axis
    plt.ylabel('Rank')

    # giving a title to my graph
    plt.title('Rank experiments - depth ' + depth)

    # function to show the plot
    plt.show()


def get_color_from_rank(rank):
    if rank >= 5:
        color = 'lime'
    elif 3.5 <= rank < 5:
        color = 'yellowgreen'
    elif 2 <= rank < 3.5:
        color = 'orange'
    elif 1 <= rank < 2:
        color = 'red'
    else:
        color = 'black'
    return color


def get_color_from_time(seconds):
    if seconds == -1:
        return 'black'
    if seconds < 1:
        color = 'lime'
    elif 1 <= seconds < 2.5:
        color = 'yellowgreen'
    elif 2.5 <= seconds < 7.5:
        color = 'darkolivegreen'
    elif 7.5 <= seconds < 12.5:
        color = 'yellow'
    elif 12.5 <= seconds < 30:
        color = 'orange'
    elif 30 <= seconds < 45:
        color = 'darkred'
    elif 45 <= seconds < 120:
        color = 'red'
    else:
        color = 'red'
    return color


if __name__ == '__main__':
    # Time:
    print_time_grpah(f_name='..\\results\\time_results.csv')

    # Parms:
    params_files = ['..\\results\\params_results_0_4.csv', '..\\results\\params_results_0_6.csv']
    for f_name in params_files:
        print_params_graph(f_name=f_name)

    # Rank:
    rank_file = '..\\results\\rank_results_dep_{}.csv'
    for i in [2, 3, 4, 5, 6]:
        print_rank_graph(f_name=rank_file.format(str(i)), depth=str(i))
