#!/bin/bash
#SBATCH --mem=50g
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --gres=gpu:8
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=aviv.slobodkin@mail.huji.ac.il
#SBATCH --output=/cs/snapless/oabend/lovodkin93/encoder_masking/slurm/de-en%j.out

source /cs/labs/oabend/lovodkin93/anaconda3/envs/encoder_masking/bin/activate

source_file=/cs/snapless/oabend/borgr/SSMT/preprocess/data/en_de/5.8/train.clean.unesc.tok.tc.en
target_dir=/cs/snapless/oabend/lovodkin93/encoder_masking/de-en/pre_process_same_scene_mask/en/seperated_unsegmented_data
echo "start!"
python3 seperate_data.py $source_file -o $target_dir/1-1m/1-1m.txt --max=1000000
echo "finished first million"
python3 seperate_data.py $source_file -o $target_dir/1m-2m/1m-2m.txt --min=1000000 --max=2000000
echo "finished second million"
python3 seperate_data.py $source_file -o $target_dir/2m-3m/2m-3m.txt --min=2000000 --max=3000000
echo "finished third million"
python3 seperate_data.py $source_file -o $target_dir/3m-4m/3m-4m.txt --min=3000000 --max=4000000
echo "finished fourth million"
python3 seperate_data.py $source_file -o $target_dir/4m-end/4m-end.txt --min=4000000
echo "finished!"

