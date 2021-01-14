#!/bin/bash

#SBATCH --mem=100m
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --gres=gpu:2
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=aviv.slobodkin@mail.huji.ac.il
#SBATCH --output=/cs/snapless/oabend/lovodkin93/encoder_masking/slurm/add_gaps_between_sentences%j.out

# explanation: adds gaps between sentences, so that we can easily pass it to Tupa
# how to use: sh add_gaps_between_sentences.sh <input (ungapped) sentences path> <output (gapped) sentences path>
source /cs/labs/oabend/lovodkin93/anaconda3/envs/encoder_masking/bin/activate

input_file_path=$1
output_file_path=$2

echo "start adding gaps!"

if [ ! -f "$input_file_path" ]; then
  >&2 echo "${input_file_path} does not exist"
fi

if [ -f "$output_file_path" ]; then
  echo "${output_file_path} already exists. It is first deleted, then recreated."
  rm -rf $output_file_path
fi



python3 add_gaps_between_sentences.py $input_file_path -o $output_file_path
echo "end adding gaps."
echo "Saved to ${output_file_path}"