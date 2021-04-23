#!/bin/bash
# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

function run_time_test_alpha_beta() {
	echo "------------------------------------"
	params="--player1 alpha_beta --player2 random --max_time 420 --max_moves 50"
	for depth in 2 3 4 5 6
	do
		params_final="--max_depth1 $depth $params"
		f_name="normal_${depth}"
		echo "python main.py $params_final"
		python main.py $params_final  > ./tmp/$f_name &
	done
	wait
	echo "Done ..."
	echo "------------------------------------"
}

function run_time_test() {
	echo "------------------------------------"
	params="--player1 alpha_beta --filter1 --player2 random --max_time 420 --max_moves 50"
	for keep_rate in 0.1 0.2 0.35 0.5 0.75 0.9
	do
		params_f_rate="--keep_rate $keep_rate $params"
		for depth in 2 3 4 5 6
		do
		   params_final="--max_depth1 $depth $params_f_rate"
		   f_name="${keep_rate}_${depth}"
		   echo "python main.py $params_final"
		   python main.py $params_final  > ./tmp/$f_name &
		done
	done
	wait
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
run_time_test_alpha_beta
run_time_test
print_data





