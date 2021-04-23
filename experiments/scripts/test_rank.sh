#!/bin/bash
# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

function run_wins_test() {
	echo "------------------------------------"
	params="--player1 alpha_beta --filter1 --player2 alpha_beta --max_depth1 3 --max_time 1000000000 --max_moves 1000"
	for keep_rate in 0.1 0.2 0.35 0.4 0.5 0.6 0.75 0.9
	do
		params_f_rate="--keep_rate $keep_rate $params"
		for depth in 2 3 4 5 6
		do
		   params_final="--max_depth1 $depth $params_f_rate"
		   f_name="${keep_rate}_${depth}"
		   echo "python main.py $params_final"
       for v in {1..10}
       do
         python main.py $params_final  >> ./tmp/$f_name &
       done
       wait
		done
	done
	echo "Done ..."
	echo "------------------------------------"
}

function print_data() {
  grep -c "WINNER: Player 1" "./tmp/*.txt"
  grep -c "DRAW" "./tmp/*.txt"
  grep "AVG_PLAYER_1" "./tmp/*.txt"
}

mkdir ./tmp >& /dev/null
rm ./tmp/*
run_wins_test
print_data

