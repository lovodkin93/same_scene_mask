import numpy as np
import pickle
import argparse
SAVE_NOT_SEG_TO_FILE=True
desc="unsegment words in sentences and build a dictionary that maps every segment to the full word it was segmented from"


# sent_src_data_path = "/cs/snapless/oabend/borgr/SSMT/preprocess/data/en_de/5.8/train.clean.unesc.tok.tc.bpe.de"
# sent_trgt_path = "/cs/snapless/oabend/lovodkin93/encoder_masking/de-en/merged_sentences_and_maps/de/"
# sent_trgt_data_path = sent_trgt_path + "train_not_seg_sents.txt"
# pickle_path = sent_trgt_path + "words_maps.pickle"
# sent_src_data_path="../train.clean.unesc.tok.tc.bpe.de"
# sent_trgt_data_path="train_not_seg_sents.txt"
# pickle_path="words_maps.pickle"




def add_to_map(maps, i, j, concat_list):
    clean_concat_list = [elem.replace('@@', '') for elem in concat_list]
    maps[i][j] = concat_list
    return [], maps

def main(args):
    sent_src_data_path = args.filenames[0]
    #sent_trgt_data_path = args.outdir
    pickle_path = args.outdir_map
    
    
    
    sent_src_file = open(sent_src_data_path, 'r')
    # if SAVE_NOT_SEG_TO_FILE:
    #     sent_trgt_file = open(sent_trgt_data_path,'w')

    sentences = sent_src_file.readlines()
    maps = dict()
    concat_list = []
    for i,sent in enumerate(sentences):
        maps[i] = dict()
        split_sent = sent.split()
        cnt=0
        for word in split_sent:
            if word.endswith('@@'):
                concat_list.append(word)
            else:
                concat_list.append(word)
                maps[i][cnt] = concat_list
                cnt+=1
                concat_list=[]
        # full_sentence = ' '.join([key for key in maps[i].keys()])
        # if SAVE_NOT_SEG_TO_FILE:
        #     sent_trgt_file.writelines(full_sentence)
        #     sent_trgt_file.writelines('\n')

    sent_src_file.close()

    # if SAVE_NOT_SEG_TO_FILE:
    #     sent_trgt_file.close()

    with open(pickle_path, 'wb') as handle:
        pickle.dump(maps, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #how to read the maps again:
    with open(pickle_path, 'rb') as handle:
        b = pickle.load(handle)
    if maps == b:
        print("equal!")



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("filenames", nargs="+", help=desc)
    argparser.add_argument("-m", "--outdir_map", default=".", help="output map (segments to full words) path")
    # argparser.add_argument("-o", "--outdir", default=".", help="output file text path")
    main(argparser.parse_args())