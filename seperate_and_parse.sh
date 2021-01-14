#!/bin/bash

#SBATCH --mem=100m
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --gres=gpu:4
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=aviv.slobodkin@mail.huji.ac.il
#SBATCH --output=/cs/snapless/oabend/lovodkin93/encoder_masking/slurm/seperate_and_parse%j.out

# explanation: unsegments the input file's sentence, saves a map between the segmenets and the full word they came from and UCCA parses the unsegmented version with the UCCA parser given
# how to use: sh seperate_and_parse.sh <input sentences path> <unsegmented target file path> <map (segments to full word) path> <xml target directory> <ucca parser path> <language (en/de/fr/ru...)> <bert/no_bert>


source /cs/labs/oabend/lovodkin93/anaconda3/envs/encoder_masking/bin/activate
#input_file_path=/cs/snapless/oabend/lovodkin93/encoder_masking/de-en/same_scene_masks_scripts/train_not_seg_sents.txt
input_file_path=$1
full_sent_path=$2
maps_path=$3
output_xml_dir=$4
ucca_parser_path=$5
lang=$6
isBert=$7
MAX_SENT_PER_BATCH=2

echo "start!"
sep_sent_dir=seperated_$lang

# unsegment the sentences and build build the dictionary that maps every segment to its unsegmented word
python3 merge_segments.py $input_file_path -o -m $maps_path
echo "ended unsegmenting"



# seperate all the file into different files


sep_sent_dir=seperated_$lang
sent_cnt=0
batch_cnt=0

if [ -d $output_xml_dir ]; then
  rm -rf $output_xml_dir
fi
mkdir $output_xml_dir

while read p; do
    if  (( batch_cnt==0 )); then
      if [ -d $sep_sent_dir ]; then
        rm -rf $sep_sent_dir
      fi
      mkdir $sep_sent_dir

      (( proc_num= sent_cnt/MAX_SENT_PER_BATCH ))
      echo "start separation (each sentence in seperate txt file) - batch number ${proc_num}"
    fi


    echo $p >> $sep_sent_dir/${sent_cnt}.txt
    ((sent_cnt++))
    ((batch_cnt++))
    if (( batch_cnt==MAX_SENT_PER_BATCH )); then
      # reset batch_cnt
      batch_cnt=0

      echo "start UCCA parsing"
      # parse the seperated files
      if [ "$isBert" = "bert" ]; then
        python3 -m tupa $sep_sent_dir/* --lang $lang --use-bert --bert-multilingual=0 -m $ucca_parser_path -o $output_xml_dir
      else
        python3 -m tupa $sep_sent_dir/* --lang $lang -m $ucca_parser_path -o $output_xml_dir
      fi
    fi
done < $full_sent_path

rm -rf $sep_sent_dir

