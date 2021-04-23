#!/bin/bash
# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

function run() {
  params="$1"
  f_name="$2"
  echo "python main.py $params"
  for v in {1..10}
	do
	  python main.py $params  >> ./tmp/$f_name &
	done
	wait
	echo "Done"
	echo "-----------------------------------------"
}

function run_params_test() {
	echo "------------------------------------"
	params="--player1 alpha_beta --max_depth1 4 --filter1 --keep_rate 0.4 --player2 alpha_beta --max_depth2 3 --max_time 1000 --max_moves 300"
	# Define params:
	t0="--teta 0.05 --gama 0.95 ${params}"
	t1="--teta 0.15 --gama 0.85 ${params}"
	t2="--teta 0.3  --gama 0.7  ${params}"
	t3="--teta 0.45 --gama 0.55 ${params}"
	t4="--teta 0.55 --gama 0.45 ${params}"
	t5="--teta 0.7  --gama 0.3  ${params}"
	t6="--teta 0.85 --gama 0.15 ${params}"
	t7="--teta 0.95 --gama 0.05 ${params}"

  # Run:
  run "${t0}" "t_05_g_95.txt"
  run "${t1}" "t_15_g_85.txt"
  run "${t2}" "t_30_g_70.txt"
  run "${t3}" "t_45_g_55.txt"
  run "${t4}" "t_55_g_45.txt"
  run "${t5}" "t_70_g_30.txt"
  run "${t6}" "t_85_g_15.txt"
  run "${t7}" "t_95_g_05.txt"

	echo "Done All ..."
	echo "------------------------------------"
}

function print_data() {
  grep -c "WINNER: Player 1" "./tmp/*.txt"
  grep -c "DRAW" "./tmp/*.txt"
  grep "AVG_PLAYER_1" "./tmp/*.txt"
}

mkdir ./tmp >& /dev/null
rm ./tmp/*
run_params_test
print_data






