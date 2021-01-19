#!/bin/bash

#SBATCH --mem=64g
#SBATCH -c20
#SBATCH --time=7-0
#SBATCH --gres=gpu:8
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=aviv.slobodkin@mail.huji.ac.il
#SBATCH --output=/cs/snapless/oabend/lovodkin93/encoder_masking/slurm/parsing_into_one_file_seperated_en%j.out

# how to use: sh parsing_into_one_file_seperated_data.sh <input sentences path (outputs will be save there too> <path to parser model> <lang code (two letters, e.g en)> <1 if multiligual parser, and 0 otherwise>


input_dir=$1
output_dir=$input_dir
model=$2
lang=$3
multilingual=$4

echo "start first million"
sh parsing_into_one_file.sh $input_dir/1-1m/1-1m.txt $output_dir/1-1m $model $lang $multilingual
echo "finished first million"
echo "start second million"
sh parsing_into_one_file.sh $input_dir/1m-2m/1m-2m.txt $output_dir/1m-2m $model $lang $multilingual
echo "finished second million"
echo "start third million"
sh parsing_into_one_file.sh $input_dir/2m-3m/2m-3m.txt $output_dir/2m-3m $model $lang $multilingual
echo "finished third million"
echo "start fourth million"
sh parsing_into_one_file.sh $input_dir/3m-4m/3m-4m.txt $output_dir/3m-4m $model $lang $multilingual
echo "finished fourth million"
echo "start the rest (beginning of fifth million)"
sh parsing_into_one_file.sh $input_dir/4m-end/4m-end.txt $output_dir/4m-end $model $lang $multilingual
echo "finished!"





