#!/bin/bash

#SBATCH --mem=100m
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --gres=gpu:4
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=aviv.slobodkin@mail.huji.ac.il
#SBATCH --output=/cs/snapless/oabend/lovodkin93/encoder_masking/slurm/parsing_into_one_file_de%j.out

# explanation: receives a file where each line contains a sentence, and UCCA-parses each sentence seperately (but saves them all to the same txt file)
# how to use: sh parsing_into_one_file.sh <input sentences path> <output dir path (where a ucca_trees.txt file will be saved)> <path to parser model> <leng code (two letters, e.g en> <1 if multiligual parser, and 0 otherwise>
source /cs/labs/oabend/lovodkin93/anaconda3/envs/encoder_masking/bin/activate

input_file_path=$1
output_file_path=$2
model_path=$3
lang=$4
multilingual=$5


echo "start!"

if [ ! -f "$input_file_path" ]; then
  >&2 echo "${input_file_path} does not exist"
fi
if (( multilingual==1 )); then
  python3 parsing_into_one_file.py $input_file_path -o $output_file_path -m $model_path --lang $lang --use-bert --bert-multilingual=0
else
  python3 parsing_into_one_file.py $input_file_path -o $output_file_path -m $model_path --lang $lang
fi
echo "end!"
echo "Saved to ${output_file_path}"